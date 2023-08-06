# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""AutoML object in charge of orchestrating various AutoML runs for predicting models."""
from typing import Any, cast, List, Optional, Dict, Tuple, Union

import json
import math
import os
from datetime import datetime

import numpy as np
import pandas as pd
import pytz
from azureml._restclient.models import IterationTaskDto
from azureml._restclient.service_context import ServiceContext
from azureml.automl.core import dataprep_utilities, dataset_utilities, package_utilities
from azureml.automl.core._experiment_observer import ExperimentStatus
from azureml.automl.core.console_interface import ConsoleInterface
from azureml.automl.core.constants import RunHistoryEnvironmentVariableNames
from azureml.automl.core.onnx_convert import OnnxConvertConstants
from azureml.automl.core.shared import logging_utilities
from azureml.automl.core.shared._error_response_constants import ErrorCodes
from azureml.automl.core.shared.constants import TelemetryConstants
from azureml.automl.core.shared.exceptions import (
    ClientException, DataException, ErrorTypes, MissingValueException, AutoMLException, UserException)
from azureml.automl.core.shared.limit_function_call_exceptions import TimeoutException
from azureml.automl.runtime import data_transformation
from azureml.automl.runtime import fit_pipeline as fit_pipeline_helper
from azureml.automl.runtime import training_utilities
from azureml.automl.runtime._run_history import RunType
from azureml.automl.runtime._run_history.offline_automl_run import (
    OfflineAutoMLRun, OfflineAutoMLRunContext, OfflineAutoMLRunUtil)
from azureml.automl.runtime.automl_pipeline import AutoMLPipeline
from azureml.automl.runtime.automl_run_context import AutoMLAbstractRunContext
from azureml.automl.runtime.data_context import RawDataContext
from azureml.automl.runtime.data_context import TransformedDataContext
from azureml.automl.runtime.faults_verifier import VerifierManager
from azureml.automl.runtime.featurizer.transformer.featurization_utilities import skip_featurization
from azureml.automl.runtime.fit_output import FitOutput
from azureml.automl.runtime.onnx_convert import OnnxConverter
from azureml.automl.runtime.shared import memory_utilities
from azureml.automl.runtime.shared import utilities as runtime_utilities
from azureml.automl.runtime.shared.cache_store import CacheStore
from azureml.automl.runtime.shared.datasets import DatasetBase
from azureml.automl.runtime.shared.types import DataInputType
from azureml.automl.runtime.streaming_data_context import StreamingTransformedDataContext
from azureml.core import Run
from azureml.exceptions import ServiceException as AzureMLServiceException
from azureml.telemetry.contracts import Event, RequiredFields, RequiredFieldKeys, \
    StandardFields, StandardFieldKeys
from azureml.train.automl import constants
from azureml.train.automl._automl_datamodel_utilities import MODEL_EXPLAINABILITY_ID
from azureml.train.automl._azure_experiment_observer import AzureExperimentObserver
from azureml.train.automl._constants_azureml import ContinueFlagStates
from azureml.train.automl._remote_console_interface import RemoteConsoleInterface
from azureml.train.automl.automl_adb_run import AutoMLADBRun
from azureml.train.automl.constants import ComputeTargets
from azureml.train.automl.exceptions import ConfigException, ModelFitException
from azureml.train.automl.run import AutoMLRun
from azureml.train.automl.runtime import utilities as train_runtime_utilities
from azureml.train.automl.utilities import (friendly_http_exception,
                                            _get_package_version,
                                            _raise_exception)
from msrest.exceptions import HttpOperationError

from . import _automl
from ._adb_driver_node import _AdbDriverNode
from ._adb_run_experiment import adb_run_experiment
from ._azureautomlruncontext import AzureAutoMLRunContext
from ._cachestorefactory import CacheStoreFactory
from .automl_explain_utilities import _automl_perform_best_run_explain_model


class RuntimeClient:
    """Client to run AutoML experiments on Azure Machine Learning platform."""

    # Caches for querying and printing child runs
    run_map = {}
    metric_map = {}
    properties_map = {}

    def __init__(self, azureautomlclient):
        """
        Construct the AzureMLClient class.

        :param azureautomlclient: The azureml.train.automl.AzureAutoMLClient experiment
        """

        self.azureautomlclient = azureautomlclient
        self._run_best = None
        self._run_max = None
        self._run_min = None
        self._started_uploading_offline_run_history = False

    def __del__(self):
        """Clean up AutoML loggers and close files."""
        try:
            logging_utilities.cleanup_log_map(self.azureautomlclient.automl_settings.debug_log,
                                              self.azureautomlclient.automl_settings.verbosity)

            if self.azureautomlclient._usage_telemetry is not None:
                self.azureautomlclient._usage_telemetry.stop()
        except Exception:
            # last chance, nothing can be done, so ignore any exception
            pass

    def cancel(self):
        """
        Cancel the ongoing local run.

        :return: None
        """
        self.azureautomlclient._status = constants.Status.Terminated

    def _create_parent_run_for_local(self,
                                     X: Optional[DataInputType] = None,
                                     y: Optional[DataInputType] = None,
                                     sample_weight: Optional[DataInputType] = None,
                                     X_valid: Optional[DataInputType] = None,
                                     y_valid: Optional[DataInputType] = None,
                                     sample_weight_valid: Optional[DataInputType] = None,
                                     cv_splits_indices: Optional[List[Any]] = None,
                                     existing_run: bool = False,
                                     managed_run_id: Optional[str] = None,
                                     training_data: Optional[DataInputType] = None,
                                     validation_data: Optional[DataInputType] = None,
                                     verifier: Optional[VerifierManager] = None,
                                     _script_run: Optional[Run] = None) -> AutoMLRun:
        """
        Create parent run in Run History containing AutoML experiment information.

        :return: AutoML parent run
        :rtype: azureml.train.automl.AutoMLRun
        """
        #  Prepare data before entering for loop
        self.azureautomlclient.logger.info("Extracting user Data")
        self.azureautomlclient.input_data = training_utilities.format_training_data(
            X, y, sample_weight, X_valid, y_valid, sample_weight_valid,
            cv_splits_indices=cv_splits_indices, user_script=self.azureautomlclient.user_script,
            training_data=training_data, validation_data=validation_data,
            label_column_name=self.azureautomlclient.automl_settings.label_column_name,
            weight_column_name=self.azureautomlclient.automl_settings.weight_column_name,
            automl_settings=self.azureautomlclient.automl_settings,
            logger=self.azureautomlclient.logger, is_adb_run=True,
            verifier=verifier)

        if self.azureautomlclient.input_data is None:
            raise DataException("Cannot extract data from user inputs",
                                target=DataException.MISSING_DATA, has_pii=False)

        training_utilities.validate_training_data_dict(self.azureautomlclient.input_data,
                                                       self.azureautomlclient.automl_settings,
                                                       check_sparse=True)
        training_utilities.auto_blacklist(self.azureautomlclient.input_data, self.azureautomlclient.automl_settings)
        if self.azureautomlclient.automl_settings.exclude_nan_labels:
            self.azureautomlclient.input_data = runtime_utilities._y_nan_check(self.azureautomlclient.input_data)
        training_utilities.set_task_parameters(self.azureautomlclient.input_data.get('y'),
                                               self.azureautomlclient.automl_settings)
        if managed_run_id is not None:
            self.azureautomlclient.parent_run_id = managed_run_id
        if not existing_run:
            parent_run_dto = self.azureautomlclient._create_parent_run_dto(constants.ComputeTargets.LOCAL)

            if managed_run_id is None:
                try:
                    self.azureautomlclient.logger.info("Start creating parent run")
                    self.azureautomlclient.parent_run_id = self.azureautomlclient._jasmine_client.post_parent_run(
                        parent_run_dto)
                    if self.azureautomlclient.parent_run_id is None:
                        raise MissingValueException("Expected to have a valid parent run ID after posting to JOS.",
                                                    target="ParentRunId",
                                                    has_pii=False)
                    self.azureautomlclient.logger.update_default_property('parent_run_id',
                                                                          self.azureautomlclient.parent_run_id)
                except (AzureMLServiceException, HttpOperationError) as e:
                    _raise_exception(e)
                    friendly_http_exception(e, constants.API.CreateParentRun)
                except Exception as e:
                    logging_utilities.log_traceback(e, self.azureautomlclient.logger)
                    raise ClientException("Error when trying to create parent run in automl service",
                                          has_pii=False) from None

            self.azureautomlclient._jasmine_client.set_parent_run_status(
                self.azureautomlclient.parent_run_id, constants.RunState.PREPARE_RUN)

            if _script_run is not None:
                _script_run.add_properties({"automl_id": self.azureautomlclient.parent_run_id})
                r_fields = RequiredFields()
                r_fields[RequiredFieldKeys.SUBSCRIPTION_ID_KEY] = \
                    self.azureautomlclient.experiment.workspace.subscription_id
                r_fields[RequiredFieldKeys.WORKSPACE_ID_KEY] = self.azureautomlclient.experiment.workspace.name
                s_fields = StandardFields()
                s_fields[StandardFieldKeys.PARENT_RUN_ID_KEY] = self.azureautomlclient.parent_run_id
                # TODO: Log event should be exposed on the Telemetry logger.
                self.azureautomlclient.logger._event_logger.log_event(
                    Event(name="Running on local docker or local conda.",
                          required_fields=r_fields,
                          standard_fields=s_fields))
            self.azureautomlclient.current_run = AutoMLRun(
                self.azureautomlclient.experiment,
                self.azureautomlclient.parent_run_id,
                host=self.azureautomlclient.automl_settings.service_url)

            # For back compatibility, check if the properties were added already as part of create parent run dto.
            # If not, add it here. Note that this should be removed once JOS changes are stably deployed
            if (
                    self.azureautomlclient.DISPLAY_TASK_TYPE_PROPERTY not in
                    self.azureautomlclient.current_run.properties or
                    self.azureautomlclient.SDK_DEPENDENCIES_PROPERTY not in
                    self.azureautomlclient.current_run.properties
            ):
                properties_to_update = self.azureautomlclient._get_current_run_properties_to_update()
                self.azureautomlclient.current_run.add_properties(properties_to_update)

        else:
            self.azureautomlclient.current_run = AutoMLRun(
                self.azureautomlclient.experiment,
                self.azureautomlclient.parent_run_id,
                host=self.azureautomlclient.automl_settings.service_url)

        if self.azureautomlclient.user_script:
            self.azureautomlclient.logger.info("[ParentRunID:{}] Local run using user script.".format(
                self.azureautomlclient.parent_run_id))
        else:
            self.azureautomlclient.logger.info("[ParentRunID:{}] Local run using input X and y.".format(
                self.azureautomlclient.parent_run_id))

        self.azureautomlclient._console_writer.println("Parent Run ID: {}\n".format(
            self.azureautomlclient.parent_run_id))
        self.azureautomlclient.logger.info("Parent Run ID: " + self.azureautomlclient.parent_run_id)

        self.azureautomlclient._status = constants.Status.InProgress

        self._log_data_stat(self.azureautomlclient.input_data.get("X"), 'X', prefix="[ParentRunId:{}]".format(
            self.azureautomlclient.parent_run_id))
        self._log_data_stat(self.azureautomlclient.input_data.get("y"), 'y', prefix="[ParentRunId:{}]".format(
            self.azureautomlclient.parent_run_id))
        dataset_utilities.log_dataset("X", X, self.azureautomlclient.current_run)
        dataset_utilities.log_dataset("y", y, self.azureautomlclient.current_run)
        dataset_utilities.log_dataset("X_valid", X_valid, self.azureautomlclient.current_run)
        dataset_utilities.log_dataset("y_valid", y_valid, self.azureautomlclient.current_run)

        return self.azureautomlclient.current_run

    def _get_transformed_context(self,
                                 input_data: Dict[str, Any],
                                 experiment_observer: AzureExperimentObserver,
                                 cache_store: Optional[CacheStore],
                                 verifier: VerifierManager) \
            -> Union[TransformedDataContext, StreamingTransformedDataContext]:
        with self.azureautomlclient.logger.log_activity(logger=None,
                                                        activity_name=TelemetryConstants.PRE_PROCESS_NAME):
            if input_data.get("X_valid") is not None:
                self._log_data_stat(
                    input_data.get("X_valid"),
                    'X_valid', prefix="[ParentRunId:{}]".format(self.azureautomlclient.parent_run_id)
                )
            if input_data.get("y_valid") is not None:
                self._log_data_stat(
                    input_data.get("y_valid"), 'y_valid',
                    prefix="[ParentRunId:{}]".format(self.azureautomlclient.parent_run_id)
                )

            raw_data_context = RawDataContext(automl_settings_obj=self.azureautomlclient.automl_settings,
                                              X=input_data.get("X"),
                                              y=input_data.get("y"),
                                              X_valid=input_data.get("X_valid"),
                                              y_valid=input_data.get("y_valid"),
                                              sample_weight=input_data.get("sample_weight"),
                                              sample_weight_valid=input_data.get("sample_weight_valid"),
                                              x_raw_column_names=input_data.get("x_raw_column_names"),
                                              cv_splits_indices=input_data.get("cv_splits_indices"))

            feature_sweeping_config = self.azureautomlclient.feature_config_manager.get_feature_sweeping_config(
                self.azureautomlclient.automl_settings.enable_feature_sweeping,
                self.azureautomlclient.parent_run_id,
                self.azureautomlclient.automl_settings.task_type)
            transformed_data_context = data_transformation.transform_data(
                raw_data_context=raw_data_context,
                experiment_observer=experiment_observer,
                logger=self.azureautomlclient.logger,
                cache_store=cache_store,
                is_onnx_compatible=self.azureautomlclient.automl_settings.enable_onnx_compatible_models,
                enable_dnn=self.azureautomlclient.automl_settings.enable_dnn,
                enable_feature_sweeping=self.azureautomlclient.automl_settings.enable_feature_sweeping,
                feature_sweeping_config=feature_sweeping_config,
                verifier=verifier)

            return transformed_data_context

    def _fit_local(self, X=None, y=None, sample_weight=None, X_valid=None, y_valid=None, sample_weight_valid=None,
                   cv_splits_indices=None, existing_run=False,
                   training_data=None, validation_data=None, _script_run=None):
        # Start telemetry in local training
        self.azureautomlclient._usage_telemetry.start()

        verifier = VerifierManager()

        self._create_parent_run_for_local(
            X=X, y=y, sample_weight=sample_weight, X_valid=X_valid, y_valid=y_valid,
            cv_splits_indices=cv_splits_indices, existing_run=existing_run,
            managed_run_id=self.azureautomlclient.automl_settings._local_managed_run_id,
            sample_weight_valid=sample_weight_valid,
            training_data=training_data, validation_data=validation_data, verifier=verifier, _script_run=_script_run)

        if not self.azureautomlclient.automl_settings._ignore_package_version_incompatibilities:
            package_utilities._ensure_package_compatibility(package_utilities.AUTOML_PACKAGES,
                                                            package_utilities._PACKAGES_TO_IGNORE_VERSIONS)

        # Init the onnx converter with the original X if user set wants to enable onnx compatible models.
        if self.azureautomlclient.automl_settings.enable_onnx_compatible_models:
            pkg_ver = _get_package_version()
            enable_split_onnx_models = \
                self.azureautomlclient.automl_settings.enable_split_onnx_featurizer_estimator_models
            self.azureautomlclient.onnx_cvt = OnnxConverter(
                logger=self.azureautomlclient.logger,
                version=pkg_ver,
                is_onnx_compatible=self.azureautomlclient.automl_settings.enable_onnx_compatible_models,
                enable_split_onnx_featurizer_estimator_models=enable_split_onnx_models)
            onnx_mdl_name = '{}[{}]'.format(OnnxConvertConstants.OnnxModelNamePrefix,
                                            self.azureautomlclient.parent_run_id)
            onnx_mdl_desc = {'ParentRunId': self.azureautomlclient.parent_run_id}
            self.azureautomlclient.onnx_cvt.initialize_input(
                X=self.azureautomlclient.input_data.get("X"),
                x_raw_column_names=self.azureautomlclient.input_data.get("x_raw_column_names"),
                model_name=onnx_mdl_name,
                model_desc=onnx_mdl_desc)

        # `enable_cache` is deprecated. Instead, rely on either `featurization` or `is_timeseries` flags to
        # save the featurized / transformed data to the local disk based cache.
        cache_store = CacheStoreFactory.get_cache_store(
            enable_cache=(self.azureautomlclient.automl_settings.enable_cache or
                          not skip_featurization(self.azureautomlclient.automl_settings.featurization) or
                          self.azureautomlclient.automl_settings.is_timeseries),
            temp_location=self.azureautomlclient.automl_settings.path,
            run_target=ComputeTargets.LOCAL,
            run_id=self.azureautomlclient.parent_run_id)
        experiment_observer = AzureExperimentObserver(self.azureautomlclient.current_run,
                                                      self.azureautomlclient._console_writer,
                                                      self.azureautomlclient.logger)
        transformed_data_context = self._get_transformed_context(self.azureautomlclient.input_data,
                                                                 experiment_observer,
                                                                 cache_store,
                                                                 verifier)

        if not existing_run:
            self.azureautomlclient._jasmine_client.set_parent_run_status(
                self.azureautomlclient.parent_run_id, constants.RunState.START_RUN)

            # set the problem info, so the JOS can use it to get pipelines.
            _automl._set_problem_info(transformed_data_context.X,
                                      transformed_data_context.y,
                                      automl_settings=self.azureautomlclient.automl_settings,
                                      current_run=self.azureautomlclient.current_run,
                                      transformed_data_context=transformed_data_context,
                                      cache_store=cache_store,
                                      logger=self.azureautomlclient.logger)

        subsampling = self.azureautomlclient.current_run._get_problem_info_dict().get('subsampling', False)

        dataset = training_utilities.init_client_dataset(
            transformed_data_context=cast(TransformedDataContext, transformed_data_context),
            cache_store=cache_store,
            automl_settings=self.azureautomlclient.automl_settings,
            remote=False,
            init_all_stats=False,
            keep_in_memory=False
        )
        self.azureautomlclient.logger.info(
            "Initialized ClientDatasets object from transformed_data_context.. deleting transformed_data_context.")
        del transformed_data_context

        try:
            #  Set up interface to print execution progress
            ci = ConsoleInterface("score", self.azureautomlclient._console_writer, mask_sampling=not subsampling)
        except Exception as e:
            logging_utilities.log_traceback(e, self.azureautomlclient.logger)
            raise

        self.azureautomlclient.experiment_start_time = datetime.utcnow()

        parent_run_context = AzureAutoMLRunContext(self.azureautomlclient.current_run)

        if existing_run:
            self.azureautomlclient.current_run.tag("continue", ContinueFlagStates.ContinueSet)
            self.azureautomlclient.current_iter = len(
                list(self.azureautomlclient.current_run.get_children(_rehydrate_runs=False)))
        else:
            self.azureautomlclient.current_iter = 0
            if verifier is not None:
                verifier.write_result_file(
                    parent_run_context,
                    self.azureautomlclient.logger,
                    working_directory=self.azureautomlclient.automl_settings.path)
                ci.print_guardrails(verifier.ret_dict['faults'])

        self.azureautomlclient.logger.info("Beginning model selection.")
        experiment_observer.report_status(ExperimentStatus.ModelSelection, "Beginning model selection.")
        ci.print_descriptions()
        ci.print_columns()

        # Get the community or premium config
        feature_configs = self.azureautomlclient.feature_config_manager.get_feature_configurations(
            self.azureautomlclient.parent_run_id,
            model_explainability=self.azureautomlclient.automl_settings.model_explainability)

        fit_outputs = []  # type: List[FitOutput]

        try:
            self.azureautomlclient.logger.info("Starting local loop.")

            while self.azureautomlclient.current_iter < self.azureautomlclient.automl_settings.iterations:
                if self.azureautomlclient._status == constants.Status.Terminated:
                    self.azureautomlclient._console_writer.println(
                        "Stopping criteria reached at iteration {0}. Ending experiment.".format(
                            self.azureautomlclient.current_iter - 1))
                    self.azureautomlclient.logger.info(
                        "Stopping criteria reached at iteration {0}. Ending experiment.".format(
                            self.azureautomlclient.current_iter - 1))
                    break
                self.azureautomlclient.logger.info("Start iteration: {0}".format(self.azureautomlclient.current_iter))
                with self.azureautomlclient.logger.log_activity(logger=None,
                                                                activity_name=TelemetryConstants.FIT_ITERATION_NAME):
                    fit_output = self._fit_iteration(
                        fit_outputs, ci, dataset=dataset, feature_configs=feature_configs)
                self.azureautomlclient.current_iter = self.azureautomlclient.current_iter + 1
                # History for a 'Continue'd run is kinda tricky to get (e.g. fetching all runs from RH),
                # and in some sense extraneous given this is an optimization primarily intended for ManyModels
                # Hence, don't cache previous outputs for a continued run, and let JOS figure it out.
                if not existing_run and fit_output:
                    fit_outputs.append(fit_output)

            # Upload summarized offline run history.
            # (Note: there will only be offline run history to upload if tracking child runs is disabled.)
            self._upload_summarized_offline_run_history(parent_run_context, fit_outputs)

            if self.azureautomlclient._is_any_childruns_succeed(
                self.azureautomlclient.current_run, self.azureautomlclient.logger
            ):
                try:
                    # Perform model explanations for best run
                    _automl_perform_best_run_explain_model(
                        self.azureautomlclient.current_run, dataset,
                        self.azureautomlclient.automl_settings,
                        self.azureautomlclient.logger,
                        compute_target=constants.ComputeTargets.LOCAL,
                        current_run=None,
                        experiment_observer=experiment_observer,
                        console_interface=ci,
                        model_exp_feature_config=feature_configs.get(MODEL_EXPLAINABILITY_ID))
                except Exception:
                    pass

                self.azureautomlclient.current_run.set_tags({
                    'best_score': str(self.azureautomlclient._score_best),
                    'best_pipeline': str(self.azureautomlclient._model_best)
                })

                self._set_parent_run_status(constants.RunState.COMPLETE_RUN)
            else:
                error_msg = "All child runs failed."
                if all(ErrorCodes.USER_ERROR == fo.failure_reason for fo in fit_outputs):
                    # All iterations failed with user errors
                    raise UserException.create_without_pii(error_msg)
                raise ModelFitException.create_without_pii(error_msg)
        except KeyboardInterrupt:
            # (Note for when not tracking child runs: in the case of a keyboard interrupt, we forgo uploading
            # summarized offline run history. This is because we're viewing a KeyboardInterrupt here as the user's
            # quick attempt @ Ctrl + C before taking more drastic measures to kill the process. We can take the
            # time after Ctrl + C to set essential state, but if we take too long / abuse this window (by
            # uploading files, etc.), the thinking is that we may lose this opportunity altogether.)
            self.azureautomlclient.logger.info(
                "[ParentRunId:{}]Received interrupt. Returning now.".format(self.azureautomlclient.parent_run_id))
            self.azureautomlclient._console_writer.println("Received interrupt. Returning now.")
            self._set_parent_run_status(constants.RunState.CANCEL_RUN)
        except (UserException, ModelFitException) as e:
            self.azureautomlclient._console_writer.println("No successful child runs.")
            self._set_parent_run_status(constants.RunState.FAIL_RUN, error_details=e,
                                        logger=self.azureautomlclient.logger)
            self._upload_summarized_offline_run_history_safe(parent_run_context, fit_outputs)
        except Exception as e:
            if self.azureautomlclient._is_any_childruns_succeed(
                self.azureautomlclient.current_run, self.azureautomlclient.logger
            ):
                self.azureautomlclient._console_writer.println(
                    "Exception thrown. Cancelling run, since there is at least one successful child run.")
                self._set_parent_run_status(constants.RunState.CANCEL_RUN, error_details=e,
                                            logger=self.azureautomlclient.logger)
            else:
                self.azureautomlclient._console_writer.println("Exception thrown. Terminating run.")
                self._set_parent_run_status(constants.RunState.FAIL_RUN, error_details=e,
                                            logger=self.azureautomlclient.logger)
            self._upload_summarized_offline_run_history_safe(parent_run_context, fit_outputs)
        finally:
            # cleanup transformed, featurized data cache
            if dataset is not None:
                cache_clear_status = dataset.clear_cache()
                if not cache_clear_status:
                    self.azureautomlclient.logger.warning("Failed to unload the dataset from cache store.")

            # if we are from continue run, remove flag
            if existing_run:
                self.azureautomlclient.current_run.tag("continue", ContinueFlagStates.ContinueNone)

            # turn off system usage collection on run completion or failure
            if self.azureautomlclient._usage_telemetry is not None:
                self.azureautomlclient._usage_telemetry.stop()

            self.azureautomlclient.logger.info("Run Complete.")

    def _set_parent_run_status(self, status, error_details=None, logger=None):
        if status == constants.RunState.COMPLETE_RUN:
            self.azureautomlclient._jasmine_client.set_parent_run_status(
                self.azureautomlclient.parent_run_id, constants.RunState.COMPLETE_RUN)
            self.azureautomlclient._status = constants.Status.Completed
        elif status == constants.RunState.CANCEL_RUN:
            self.azureautomlclient._status = constants.Status.Terminated
            self.azureautomlclient._jasmine_client.set_parent_run_status(
                self.azureautomlclient.parent_run_id, constants.RunState.CANCEL_RUN)
        elif status == constants.RunState.FAIL_RUN:
            self.azureautomlclient._fail_parent_run(error_details=error_details, logger=logger)
            self.azureautomlclient._status = constants.Status.Terminated
        if error_details is not None:
            self.azureautomlclient.current_run.add_properties({
                'error_code': getattr(error_details, 'error_code', ErrorTypes.Unclassified),
                'failure_reason': getattr(error_details, 'error_type', ErrorTypes.Unclassified)
            })

    def _fit_iteration(self,
                       previous_fit_outputs: List[FitOutput],
                       ci: ConsoleInterface,
                       transformed_data_context: Optional[TransformedDataContext] = None,
                       dataset: Optional[DatasetBase] = None,
                       feature_configs: Optional[Dict[str, Any]] = None) -> Optional[FitOutput]:
        start_iter_time = datetime.utcnow().replace(tzinfo=pytz.UTC)

        #  Query Jasmine for the next set of pipelines to run
        task_dto = self.azureautomlclient._get_task(previous_fit_outputs)

        if task_dto.is_experiment_over:
            self.azureautomlclient.logger.info("Complete task received. Completing experiment")
            self.azureautomlclient.cancel()
            return None

        pipeline_id = task_dto.pipeline_id
        pipeline_script = task_dto.pipeline_spec
        train_frac = float(task_dto.training_percent or 100) / 100

        """
        # TODO: Fix pipeline spec logging (#438111)
        self.azureautomlclient.logger.info(
            "Received pipeline: {0}".format(
                logging_utilities.remove_blacklisted_logging_keys_from_json_str(
                    pipeline_script
                )
            )
        )
        """
        self.azureautomlclient.logger.info('Received pipeline ID {}'.format(pipeline_id))
        ci.print_start(self.azureautomlclient.current_iter)

        errors = []
        fit_output = None   # type: Optional[FitOutput]

        child_run = None

        try:
            child_run, automl_run_context = self._get_child_run_and_context(task_dto)

            # get total run time in seconds and convert to minutes
            elapsed_time = math.floor(
                int((datetime.utcnow() - self.azureautomlclient.experiment_start_time).total_seconds()) / 60)
            child_run.start()

            automl_pipeline = AutoMLPipeline(automl_run_context, pipeline_script, pipeline_id, train_frac)

            self._set_environment_variables_for_reconstructing_run(child_run)

            fit_output = fit_pipeline_helper.fit_pipeline(
                automl_pipeline=automl_pipeline,
                automl_settings=self.azureautomlclient.automl_settings,
                automl_run_context=automl_run_context,
                remote=False,
                logger=self.azureautomlclient.logger,
                transformed_data_context=transformed_data_context,
                dataset=dataset,
                elapsed_time=elapsed_time,
                onnx_cvt=self.azureautomlclient.onnx_cvt,
                bypassing_model_explain=self.azureautomlclient.current_run.get_tags().get('model_explain_run'),
                feature_configs=feature_configs,
                working_dir=self.azureautomlclient.automl_settings.path)

            if fit_output.errors:
                err_type = next(iter(fit_output.errors))
                exception_info = fit_output.errors[err_type]
                exception_obj = cast(BaseException, exception_info['exception'])
                if err_type == 'model_explanation' and isinstance(exception_obj, ImportError):
                    errors.append('Could not explain model due to missing dependency. Please run: pip install '
                                  'azureml-sdk[explain]')
                elif isinstance(exception_obj, TimeoutException):
                    if constants.ClientErrors.EXCEEDED_EXPERIMENT_TIMEOUT_MINUTES \
                            not in exception_obj._exception_message:
                        errors.append(exception_obj._exception_message)
                else:
                    error_msg = ' '.join(['Run {} failed with exception of type: {}.'.format(
                        task_dto.childrun_id, exception_obj.__class__.__name__), str(fit_output.pipeline_spec)])
                    if isinstance(exception_obj, AutoMLException):
                        msg = exception_obj.pii_free_msg(scrubbed=False)
                        if msg:
                            error_msg = ' '.join([str(exception_obj)])
                    errors.append(error_msg)

            score = fit_output.score
            preprocessor = fit_output.run_preprocessor
            model_name = fit_output.run_algorithm
        except Exception as e:
            logging_utilities.log_traceback(e, self.azureautomlclient.logger)
            score = constants.Defaults.DEFAULT_PIPELINE_SCORE
            preprocessor = ''
            model_name = ''
            errors.append('Run {} failed with exception of type: {}'.format(
                task_dto.childrun_id, e.__class__.__name__))

        ci.print_pipeline(preprocessor, model_name, train_frac)
        self._update_internal_scores_after_iteration(score, model_name, child_run)

        end_iter_time = datetime.utcnow().replace(tzinfo=pytz.UTC)
        start_iter_time, end_iter_time = train_runtime_utilities._calculate_start_end_times(
            start_iter_time,
            end_iter_time,
            child_run)
        iter_duration = str(end_iter_time - start_iter_time).split(".")[0]
        ci.print_end(iter_duration, score, self.azureautomlclient._score_best)

        for error in errors:
            ci.print_error(error)

        return fit_output

    def _log_data_stat(self, data, data_name, prefix=None):
        if prefix is None:
            prefix = ""
        if type(data) is not np.ndarray and type(data) is not np.array and type(data) is not pd.DataFrame:
            try:
                data = data.to_pandas_dataframe()
            except AttributeError:
                self.azureautomlclient.logger.warning("The data type is not supported for logging.")
                return
        self.azureautomlclient.logger.info(
            "{}Input {} datatype is {}, shape is {}, datasize is {}.".format(
                prefix, data_name, '[Scrubbed]', data.shape,
                memory_utilities.get_data_memory_size(data)
            )
        )

    def _get_child_run_and_context(
        self,
        task_dto: IterationTaskDto
    ) -> Tuple[RunType, AutoMLAbstractRunContext]:
        """Get child run and its associated run context."""
        if self.azureautomlclient.automl_settings.track_child_runs:
            child_run = self.azureautomlclient._create_child_run(task_dto)
            run_context = AzureAutoMLRunContext(child_run)
            return child_run, run_context
        else:
            offline_child_run = OfflineAutoMLRunUtil.create_child_run(
                path=self.azureautomlclient.automl_settings.path,
                parent_run_id=self.azureautomlclient.current_run.id,
                iteration=self.azureautomlclient.current_iter,
                pipeline_spec=task_dto.pipeline_spec)
            offline_run_context = OfflineAutoMLRunContext(offline_child_run)
            return offline_child_run, offline_run_context

    def _init_adb_driver_run(self,
                             run_configuration=None,
                             X=None,
                             y=None,
                             sample_weight=None,
                             X_valid=None,
                             y_valid=None,
                             sample_weight_valid=None,
                             cv_splits_indices=None,
                             training_data=None,
                             validation_data=None,
                             show_output=False,
                             existing_run=False):

        self.azureautomlclient._console_writer.println(
            'Running an experiment on spark cluster: {0}.\n'.format(self.azureautomlclient.automl_settings.name))

        # Forecasting runs will fail if caching is turned off (ADB only)
        if self.azureautomlclient.automl_settings.is_timeseries and not \
                self.azureautomlclient.automl_settings.enable_cache:
            raise ConfigException.create_without_pii(
                'Time-series forecasting requires `enable_cache=True` on spark cluster.')

        try:
            if not existing_run:
                self.azureautomlclient._fit_remote_core(run_configuration,
                                                        X=X,
                                                        y=y,
                                                        sample_weight=sample_weight,
                                                        X_valid=X_valid,
                                                        y_valid=y_valid,
                                                        sample_weight_valid=sample_weight_valid,
                                                        cv_splits_indices=cv_splits_indices,
                                                        training_data=training_data,
                                                        validation_data=validation_data)
            # This should be refactored to have RunHistoryClient and make call on it to get token
            token_res = self.azureautomlclient.experiment_client._client.run.\
                get_token(experiment_name=self.azureautomlclient.automl_settings.name,
                          resource_group_name=self.azureautomlclient.automl_settings.resource_group,
                          subscription_id=self.azureautomlclient.automl_settings.subscription_id,
                          workspace_name=self.azureautomlclient.automl_settings.workspace_name,
                          run_id=self.azureautomlclient.current_run.run_id)
            aml_token = token_res.token
            aml_token_expiry = token_res.expiry_time_utc

            service_context = ServiceContext(
                subscription_id=self.azureautomlclient.automl_settings.subscription_id,
                resource_group_name=self.azureautomlclient.automl_settings.resource_group,
                workspace_name=self.azureautomlclient.automl_settings.workspace_name,
                workspace_id=self.azureautomlclient.experiment.workspace._workspace_id,
                workspace_discovery_url=self.azureautomlclient.experiment.workspace.discovery_url,
                authentication=self.azureautomlclient.experiment.workspace._auth_object)

            run_history_url = service_context._get_run_history_url()
            fn_script = None
            if self.azureautomlclient.automl_settings.data_script:
                with open(self.azureautomlclient.automl_settings.data_script, "r") as f:
                    fn_script = f.read()

            if training_data is None and validation_data is None:
                dataprep_json = dataprep_utilities.get_dataprep_json(
                    X=X,
                    y=y,
                    sample_weight=sample_weight,
                    X_valid=X_valid,
                    y_valid=y_valid,
                    sample_weight_valid=sample_weight_valid,
                    cv_splits_indices=cv_splits_indices)
            else:
                dataprep_json = dataprep_utilities.get_dataprep_json_dataset(
                    training_data=training_data, validation_data=validation_data)

            # build dictionary of context
            run_context = {"subscription_id": self.azureautomlclient.automl_settings.subscription_id,
                           "resource_group": self.azureautomlclient.automl_settings.resource_group,
                           "location": self.azureautomlclient.experiment.workspace.location,
                           "workspace_name": self.azureautomlclient.automl_settings.workspace_name,
                           "experiment_name": self.azureautomlclient.automl_settings.name,
                           "experiment_id": self.azureautomlclient.experiment.id,
                           "parent_run_id": self.azureautomlclient.current_run.run_id,
                           "aml_token": aml_token,
                           "aml_token_expiry": aml_token_expiry,
                           "service_url": run_history_url,
                           "discovery_url": service_context._get_discovery_url(),
                           "automl_settings_str": json.dumps(
                               self.azureautomlclient.automl_settings.as_serializable_dict()),
                           'dataprep_json': dataprep_json,
                           "get_data_content": fn_script}
            adb_automl_context = [(index, run_context) for index in range(
                0, self.azureautomlclient.automl_settings.max_concurrent_iterations)]

            if not hasattr(self.azureautomlclient.automl_settings, 'is_run_from_test'):
                adb_thread = _AdbDriverNode("AutoML on Spark Experiment: {0}".format(
                    self.azureautomlclient.experiment.name),
                    adb_automl_context,
                    self.azureautomlclient.automl_settings.spark_context,
                    self.azureautomlclient.automl_settings.max_concurrent_iterations,
                    self.azureautomlclient.current_run.run_id)
                adb_thread.start()
                self.azureautomlclient.current_run = AutoMLADBRun(
                    self.azureautomlclient.experiment,
                    self.azureautomlclient.parent_run_id,
                    adb_thread)
            else:
                automlRDD = self.azureautomlclient.automl_settings.\
                    spark_context.parallelize(adb_automl_context,
                                              self.azureautomlclient.automl_settings.max_concurrent_iterations)
                automlRDD.map(adb_run_experiment).collect()

            if show_output:
                RemoteConsoleInterface._show_output(self.azureautomlclient.current_run,
                                                    self.azureautomlclient._console_writer,
                                                    self.azureautomlclient.logger,
                                                    self.azureautomlclient.automl_settings.primary_metric)
        except Exception as ex:
            logging_utilities.log_traceback(ex, self.azureautomlclient.logger)
            raise

    def _update_internal_scores_after_iteration(self, score, model_name, run):
        if self.azureautomlclient._score_max is None or \
                np.isnan(self.azureautomlclient._score_max) or \
                score > self.azureautomlclient._score_max:
            self.azureautomlclient._score_max = score
            self.azureautomlclient._model_max = model_name
            self._run_max = run
        if self.azureautomlclient._score_min is None or \
                np.isnan(self.azureautomlclient._score_min) or \
                score < self.azureautomlclient._score_min:
            self.azureautomlclient._score_min = score
            self.azureautomlclient._model_min = model_name
            self._run_min = run

        if self.azureautomlclient.automl_settings.metric_operation == constants.OptimizerObjectives.MINIMIZE:
            self.azureautomlclient._score_best = self.azureautomlclient._score_min
            self.azureautomlclient._model_best = self.azureautomlclient._model_min
            self._run_best = self._run_min
        elif self.azureautomlclient.automl_settings.metric_operation == constants.OptimizerObjectives.MAXIMIZE:
            self.azureautomlclient._score_best = self.azureautomlclient._score_max
            self.azureautomlclient._model_best = self.azureautomlclient._model_max
            self._run_best = self._run_max

    def _set_environment_variables_for_reconstructing_run(
        self,
        run: RunType
    ) -> None:
        """Copy the run information to environment variables. This allows a child process to reconstruct the
        run object."""
        if self.azureautomlclient.automl_settings.track_child_runs:
            self.azureautomlclient._set_environment_variables_for_reconstructing_run(run)
        else:
            os.environ[RunHistoryEnvironmentVariableNames.AZUREML_RUN_ID] = run.id
            os.environ[RunHistoryEnvironmentVariableNames.AZUREML_AUTOML_RUN_HISTORY_DATA_PATH] = \
                OfflineAutoMLRunUtil.get_run_history_data_folder(
                path=self.azureautomlclient.automl_settings.path,
                parent_run_id=self.azureautomlclient.parent_run_id)

    def _upload_summarized_offline_run_history(
        self,
        parent_run_context: AzureAutoMLRunContext,
        fit_outputs: List[FitOutput]
    ) -> None:
        """Summarize and upload unprocessed offline run history."""
        # If tracking child runs, return.
        # (There is only offline run history to process if not tracking child runs.)
        if self.azureautomlclient.automl_settings.track_child_runs:
            return

        # If you could have started
        if self._started_uploading_offline_run_history:
            return

        self._started_uploading_offline_run_history = True

        if not self._run_best:
            self.azureautomlclient.logger.info(
                "Best child run cannot be found. Aborting upload of offline run history")
            return

        # Create a single child run of the parent run in RH, with the suffix '_best'.
        # Upload the metrics, tags, etc. of the best child run to this '_best' run.
        train_runtime_utilities._create_best_run(
            parent_run=self.azureautomlclient.current_run,
            best_offline_run=cast(OfflineAutoMLRun, self._run_best),
            logger=self.azureautomlclient.logger)

        # Upload summary of child iterations to the parent run
        train_runtime_utilities._upload_summary_of_iterations(
            logger=self.azureautomlclient.logger,
            parent_run_context=parent_run_context,
            fit_outputs=fit_outputs)

    def _upload_summarized_offline_run_history_safe(
        self,
        parent_run_context: AzureAutoMLRunContext,
        fit_outputs: List[FitOutput]
    ) -> None:
        """Upload summarized offline run history while catching & logging any thrown exceptions."""
        try:
            self._upload_summarized_offline_run_history(parent_run_context, fit_outputs)
        except Exception as e:
            logging_utilities.log_traceback(e, self.azureautomlclient.logger)
