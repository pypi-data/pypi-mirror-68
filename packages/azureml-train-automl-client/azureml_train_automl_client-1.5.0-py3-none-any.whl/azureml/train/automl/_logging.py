# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Auto ML common logging module."""
from typing import Any, Dict, Optional, TYPE_CHECKING
import logging
import pkg_resources

from azureml.telemetry import AML_INTERNAL_LOGGER_NAMESPACE, get_telemetry_log_handler
from azureml.telemetry.contracts import (RequiredFields,
                                         RequiredFieldKeys,
                                         StandardFields,
                                         StandardFieldKeys,
                                         ExtensionFields,
                                         ExtensionFieldKeys
                                         )
from .constants import ComputeTargets
from ._telemetry_activity_logger import TelemetryActivityLogger, _AutoMLExtensionFieldKeys
from .utilities import _InternalComputeTypes

TELEMETRY_AUTOML_COMPONENT_KEY = 'automl'


if TYPE_CHECKING:
    from ._azureautomlsettings import AzureAutoMLSettings


def get_azureml_logger(
    automl_settings: 'Optional[AzureAutoMLSettings]',
    parent_run_id: Optional[str],
    child_run_id: Optional[str],
    log_file_name: Optional[str] = None,
    parent_run_uuid: Optional[str] = None,
    child_run_uuid: Optional[str] = None,
) -> TelemetryActivityLogger:
    """
    Create the logger with telemetry hook.

    :param automl_settings: the AutoML settings object
    :param parent_run_id: parent run id
    :param child_run_id: child run id
    :param log_file_name: log file name
    :param parent_run_uuid: Parent run UUID
    :param child_run_uuid: Child run UUID
    :return logger if log file name is provided otherwise null logger
    :rtype
    """
    if log_file_name is None and automl_settings is not None:
        log_file_name = automl_settings.debug_log

    telemetry_handler = get_telemetry_log_handler(component_name=TELEMETRY_AUTOML_COMPONENT_KEY)

    azure_automl_sdk_version = pkg_resources.get_distribution("azureml-train-automl-client").version
    automl_core_sdk_version = pkg_resources.get_distribution("azureml-automl-core").version

    custom_dimensions = {
        "automl_client": "azureml",
        "automl_sdk_version": azure_automl_sdk_version,
        "automl_core_sdk_version": automl_core_sdk_version
    }  # type: Dict[str, Optional[Any]]

    required_fields = RequiredFields()
    standard_fields = StandardFields()
    extension_fields = ExtensionFields()

    required_fields[RequiredFieldKeys.CLIENT_TYPE_KEY] = "sdk"
    required_fields[RequiredFieldKeys.CLIENT_VERSION_KEY] = azure_automl_sdk_version
    required_fields[RequiredFieldKeys.COMPONENT_NAME_KEY] = TELEMETRY_AUTOML_COMPONENT_KEY

    extension_fields[_AutoMLExtensionFieldKeys.AUTOML_SDK_VERSION_KEY] = azure_automl_sdk_version
    extension_fields[_AutoMLExtensionFieldKeys.AUTOML_CORE_SDK_VERSION_KEY] = automl_core_sdk_version
    extension_fields[ExtensionFieldKeys.DISK_USED_KEY] = None

    if automl_settings is not None:
        if automl_settings.is_timeseries:
            task_type = "forecasting"
        else:
            task_type = automl_settings.task_type

        # Override compute target based on environment.
        compute_target = _InternalComputeTypes.identify_compute_type(compute_target=automl_settings.compute_target,
                                                                     azure_service=automl_settings.azure_service)
        if not compute_target:
            if automl_settings.compute_target == ComputeTargets.LOCAL:
                compute_target = _InternalComputeTypes.LOCAL
            elif automl_settings.compute_target == ComputeTargets.AMLCOMPUTE:
                compute_target = _InternalComputeTypes.AML_COMPUTE
            elif automl_settings.spark_service == 'adb':
                compute_target = _InternalComputeTypes.DATABRICKS
            else:
                compute_target = _InternalComputeTypes.REMOTE

        custom_dimensions.update(
            {
                "task_type": task_type,
                "compute_target": compute_target,
                "subscription_id": automl_settings.subscription_id,
                "region": automl_settings.region
            }
        )

        standard_fields[StandardFieldKeys.ALGORITHM_TYPE_KEY] = task_type
        # Don't fill in the Compute Type as it is being overridden downstream by Execution service
        # ComputeTarget field is still logged in customDimensions that contains these values
        # standard_fields[StandardFieldKeys.COMPUTE_TYPE_KEY] = compute_target

        required_fields[RequiredFieldKeys.SUBSCRIPTION_ID_KEY] = automl_settings.subscription_id
        # Workspace name can have PII information. Therefore, not including it.
        # required_fields[RequiredFieldKeys.WORKSPACE_ID_KEY] = automl_settings.workspace_name

        verbosity = automl_settings.verbosity
    else:
        verbosity = logging.DEBUG

    logger = TelemetryActivityLogger(
        namespace=AML_INTERNAL_LOGGER_NAMESPACE,
        filename=log_file_name,
        verbosity=verbosity,
        extra_handlers=[telemetry_handler],
        custom_dimensions=custom_dimensions,
        required_fields=required_fields,
        standard_fields=standard_fields,
        extension_fields=extension_fields)

    if parent_run_id is not None:
        logger.update_default_property('parent_run_id', parent_run_id)
    if child_run_id is not None:
        logger.update_default_property('run_id', child_run_id)
    if parent_run_uuid is not None:
        logger.update_default_property('parent_run_uuid', parent_run_uuid)
    if child_run_uuid is not None:
        logger.update_default_property('run_uuid', child_run_uuid)

    return logger
