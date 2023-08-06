# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utility module for logging."""
from typing import Any, cast, Dict, List, Optional, Tuple, Union, Callable,\
    TypeVar
from types import ModuleType

import contextlib
import functools
import json
import logging
import logging.handlers as handlers
import os
import sys
import threading
import traceback
import uuid

from datetime import datetime

from azureml.automl.core.shared.constants import TelemetryConstants, DEFAULT_LOGGING_APP_NAME
from azureml.automl.core.shared.exceptions import AutoMLException, ErrorTypes, MemorylimitException, NON_PII_MESSAGE

# import telemetry package if available.
try:
    from azureml.telemetry import get_telemetry_log_handler, get_event_logger as _telemetry_event_logger
    from azureml.telemetry.logging_handler import AppInsightsLoggingHandler
    telemetry_imported = True
except ImportError:
    telemetry_imported = False


whitelisted_paths = set()
whitelisted_exception_types = {
    # 5.2 Concrete exceptions

    # These act on user data and so should be tested
    AttributeError,
    ImportError,
    IndexError,
    RecursionError,
    ReferenceError,
    TypeError,
    ZeroDivisionError,

    # These are all issues with source code
    NameError,
    NotImplementedError,
    SyntaxError,
    IndentationError,
    TabError,
    UnboundLocalError,

    # Temporarily disabling these until we have a good way to check for PII leakage
    # AssertionError,
    # EOFError,
    # FloatingPointError,
    # OverflowError,

    # 5.2.1 OS exceptions
    # BlockingIOError,
    # ChildProcessError,
    # ConnectionError,
    # BrokenPipeError,
    # ConnectionAbortedError,
    # ConnectionRefusedError,
    # ConnectionResetError,
    # InterruptedError,
    # ProcessLookupError,
    # TimeoutError
}


def mark_package_exceptions_as_loggable(module: ModuleType) -> None:
    try:
        paths = cast(Any, module).__path__
        for path in paths:
            # Any path in __path__ that is relative could be user code, don't whitelist it
            if os.path.commonprefix(['.', path]) == '':
                whitelisted_paths.add(path)
    except AttributeError:
        pass


def mark_path_as_loggable(path: str) -> None:
    whitelisted_paths.add(path)


def mark_path_as_not_loggable(path: str) -> None:
    whitelisted_paths.remove(path)


def is_non_automl_exception_whitelisted(exception: BaseException) -> bool:
    # Use direct type check instead of isinstance, because we should be subclassing AutoMLException instead of
    # those types and that is handled via a different path
    if type(exception) not in whitelisted_exception_types:
        return False

    frames = traceback.extract_tb(exception.__traceback__)
    if len(frames) == 0:
        return True
    exception_path = frames[-1].filename
    return is_path_whitelisted(exception_path)


def is_path_whitelisted(exception_path: str) -> bool:
    for path in whitelisted_paths:
        if exception_path.startswith(path):
            return True
    return False


def is_exception_stacktrace_loggable() -> bool:
    if os.environ.get('AUTOML_MANAGED_ENVIRONMENT') == '1':
        return True
    return False


def _get_pii_free_message(exception: BaseException) -> str:
    if isinstance(exception, AutoMLException):
        return exception.get_pii_free_exception_msg_format()
    elif is_non_automl_exception_whitelisted(exception):
        return str(exception)
    else:
        return NON_PII_MESSAGE


file_handlers = {}  # type: Dict[str, logging.Handler]
log_cache_lock = threading.Lock()
file_loggers = {}   # type: Dict[Tuple[str, int], logging.Logger]


def _get_null_logger(name: str = 'null_logger') -> logging.Logger:
    null_logger = logging.getLogger(name)
    null_logger.addHandler(logging.NullHandler())
    null_logger.propagate = False
    return null_logger


class _DummyEventLogger:
    def log_event(self, telemetry_event: Any, *args: Any, **kwargs: Any) -> str:
        pass

    def flush(self) -> None:
        pass


def _dummy_event_logger() -> _DummyEventLogger:
    """
    Null event logger in case azureml.telemetry is not installed.

    :return: Null event logger.
    """
    return _DummyEventLogger()


NULL_LOGGER = _get_null_logger()


class AppInsightsPIIStrippingFormatter(logging.Formatter):
    """Formatter for exceptions being sent to Application Insights."""

    def format(self, record: logging.LogRecord) -> str:
        """
        Modify the log record to strip error messages if they originate from a non-AzureML exception, then format.

        :param record: Logging record.
        :return: Formatted record.
        """
        exception = getattr(record, 'exception_obj', None)
        if not isinstance(exception, BaseException):
            return super().format(record)

        not_available_message = '[Not available]'

        properties = getattr(record, 'properties', {})

        message = properties.get('exception_message', NON_PII_MESSAGE)
        traceback_msg = properties.get('exception_traceback', not_available_message)

        record.message = record.msg = '\n'.join([
            'Type: {}'.format(properties.get('error_type', ErrorTypes.Unclassified)),
            'Class: {}'.format(properties.get('exception_class', not_available_message)),
            'Message: {}'.format(message),
            'Traceback: {}'.format(traceback_msg),
            'ExceptionTarget: {}'.format(properties.get('exception_target', not_available_message))
        ])

        # Update exception message and traceback in extra properties as well
        properties['exception_message'] = message

        return super().format(record)


def log_traceback(exception: BaseException,
                  logger: Optional[Union[logging.Logger, logging.LoggerAdapter]],
                  override_error_msg: Optional[str] = None,
                  is_critical: Optional[bool] = True,
                  tb: Optional[Any] = None) -> None:
    """
    Log exception traces.

    :param exception: The exception to log.
    :param logger: The logger to use.
    :param override_error_msg: The message what to display that will override the current error_msg.
    :param is_critical: If is_critical, the logger will use log.critical, otherwise log.error.
    :param tb: The traceback to use for logging; if not provided, the one attached to the exception is used.
    """
    if logger is None:
        logger = NULL_LOGGER

    # Appropriately classify MemoryErrors that may pop up anywhere in our code
    if isinstance(exception, MemoryError):
        exception = MemorylimitException.from_exception(
            exception,
            "Unable to allocate enough memory for this operation. Please consider increasing available memory.")

    if override_error_msg is not None:
        error_msg = override_error_msg
    else:
        error_msg = str(exception)

    if isinstance(exception, AutoMLException):
        error_code = exception.error_code
        error_type = exception.error_type
        exception_target = exception.target
    else:
        error_code = ErrorTypes.Unclassified
        error_type = ErrorTypes.Unclassified
        exception_target = "Unspecified"

    traceback_obj = tb or exception.__traceback__ or sys.exc_info()[2]
    traceback_msg = _CustomStackSummary.get_traceback_message(traceback_obj, remove_pii=False)

    exception_class_name = exception.__class__.__name__

    # User can see original log message in their log file
    message = [
        'Type: {}'.format(error_code),
        'Class: {}'.format(exception_class_name),
        'Message: {}'.format(error_msg),
        'Traceback:', traceback_msg,
        'ExceptionTarget: {}'.format(exception_target)
    ]

    # Marking extra properties to be PII free since azureml-telemetry logging_handler is
    # not updating the extra properties after formatting.
    # Get PII free exception_message
    error_msg_without_pii = _get_pii_free_message(exception)
    # Get PII free exception_traceback
    traceback_msg_without_pii = _CustomStackSummary.get_traceback_message(traceback_obj)
    # Get PII free exception_traceback
    extra = {
        'properties': {
            'error_code': error_code,
            'error_type': error_type,
            'exception_class': exception_class_name,
            'exception_message': error_msg_without_pii,
            'exception_traceback': traceback_msg_without_pii,
            'exception_target': exception_target
        },
        'exception_obj': exception,
        'exception_tb_obj': traceback_obj
    }
    if is_critical:
        logger.critical('\n'.join(message), extra=extra)
    else:
        logger.error('\n'.join(message), extra=extra)


def get_event_logger() -> Any:
    """
    Create event logger hooked up to AppInsights.

    :return: Event logger.
    """
    if telemetry_imported:
        return _telemetry_event_logger()

    return _dummy_event_logger()


def get_file_handler(filename: Optional[str] = None) -> logging.Handler:
    """
    Get a file handler for the given filename, creating it if it doesn't exist.

    NullHandler is returned if filename is None.

    :param filename: the file to write to
    :return: the file handler
    """
    if filename is None:
        return logging.NullHandler()
    with log_cache_lock:
        global file_handlers
        if filename not in file_handlers:
            handler = handlers.RotatingFileHandler(filename, maxBytes=1000000, backupCount=9)
            log_format = '%(asctime)s - %(levelname)s - %(lineno)d : %(message)s'
            formatter = logging.Formatter(log_format)
            handler.setFormatter(formatter)
            file_handlers[filename] = handler
        return file_handlers[filename]


def set_file_handler(logger: logging.Logger, filename: Optional[str] = None) -> None:
    """
    Add a file handler for the given filename to the logger, removing all other file handlers in the process.

    :param logger: the logger to add a handler to
    :param filename: the file to write to
    :return:
    """
    handler = get_file_handler(filename)
    if handler in logger.handlers:
        return
    logger.handlers = [
        h for h in logger.handlers if
        (not isinstance(h, logging.FileHandler) and not isinstance(h, logging.NullHandler))]
    logger.addHandler(handler)


def get_logger(namespace: Optional[str] = None,
               filename: Optional[str] = None,
               verbosity: int = logging.DEBUG,
               extra_handlers: Optional[List[logging.Handler]] = None,
               component_name: Optional[str] = None) -> logging.Logger:
    """
    Create the logger with telemetry hook.

    :param namespace: The namespace for the logger
    :param filename: log file name
    :param verbosity: logging verbosity
    :param extra_handlers: any extra handlers to attach to the logger
    :param component_name: component name
    :return: logger if log file name and namespace are provided otherwise null logger
    :rtype
    """
    if filename is None or namespace is None:
        return NULL_LOGGER

    with log_cache_lock:
        global file_loggers
        global file_handlers

        key = (filename, verbosity)
        if key in file_loggers:
            return file_loggers[key]

    logger_name = '%s_%s' % (filename, str(verbosity))
    logger = logging.getLogger(namespace).getChild(logger_name)
    set_file_handler(logger, filename)
    logger.setLevel(verbosity)

    if extra_handlers is not None:
        for h in extra_handlers:
            logger.addHandler(h)

    logger.propagate = False

    with log_cache_lock:
        file_loggers[key] = logger

    if telemetry_imported:
        if not _found_handler(logger, AppInsightsLoggingHandler):
            appinsights_handler = get_telemetry_log_handler(
                component_name=component_name)  # type: AppInsightsLoggingHandler
            appinsights_handler.setFormatter(AppInsightsPIIStrippingFormatter())
            logger.addHandler(appinsights_handler)
        else:
            # Check if handler contains PII formatter.
            for log_handler in logger.handlers:
                if (isinstance(log_handler, AppInsightsLoggingHandler) and
                        not isinstance(log_handler.formatter, AppInsightsPIIStrippingFormatter)):
                    log_handler.setFormatter(AppInsightsPIIStrippingFormatter())

    return logger


def cleanup_log_map(log_filename: str, verbosity: int = logging.DEBUG) -> None:
    """
    Cleanup log map.

    :param log_filename: log file name
    :param verbosity: log verbosity
    :return:
    """
    with log_cache_lock:
        logger = file_loggers.pop((log_filename, verbosity), None)
        handler = file_handlers.pop(log_filename, None)
        if handler:
            if logger:
                logger.removeHandler(handler)
            handler.close()


def cleanup_all_loggers() -> None:
    """
    Clean up all loggers without using logging.shutdown().

    :return:
    """
    with log_cache_lock:
        global file_loggers
        global file_handlers
        for k in file_loggers:
            logger = file_loggers[k]
            logger.handlers = []
        for k_tuple in file_handlers:
            handler = file_handlers[k_tuple]
            handler.close()
            del handler
        file_loggers = {}
        file_handlers = {}


def function_debug_log_wrapped(log_level: str = 'debug') -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Add logs wrapper around transformer class function."""
    def wrapper(f: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(f)
        def debug_log_wrapped(self: Any, *args: Any, **kwargs: Any) -> Any:
            self._logger_wrapper(
                log_level, "Starting {} operation of {}.".format(
                    f.__name__, self.__class__.__name__)
            )
            r = f(self, *args, **kwargs)
            self._logger_wrapper(
                log_level, "{} {} operation complete.".format(
                    self.__class__.__name__, f.__name__)
            )
            return r
        return debug_log_wrapped
    return wrapper


BLACKLISTED_LOGGING_KEYS = [
    'path', 'resource_group', 'workspace_name', 'data_script', 'debug_log',
    'label_column_name', 'weight_column_name',
    'time_column_name', 'grain_column_names', 'drop_column_names', 'compute_target', 'featurization',
    'y_min', 'y_max'
]


def remove_blacklisted_logging_keys_from_dict(dict_obj: Dict[str, Any]) -> None:
    """Recursively remove the key from a dict."""
    keys = [k for k in dict_obj.keys()]
    blacklisted_keys = set(BLACKLISTED_LOGGING_KEYS)
    for k in keys:
        if k in blacklisted_keys:
            del dict_obj[k]

    values = []                     # type: List[Any]
    values.extend(dict_obj.values())
    while len(values) > 0:
        v = values.pop()
        try:
            # Try to eval if the dictionary is stored as a string such as
            # "{'task_type':'classification','primary_metric':'AUC_weighted','debug_log':'classification.log'}"
            if isinstance(v, str) and v.startswith('{') and v.endswith('}'):
                v = eval(v)
        except TypeError:
            pass

        if isinstance(v, list):
            values.extend(v)

        if isinstance(v, dict):
            remove_blacklisted_logging_keys_from_dict(v)


def remove_blacklisted_logging_keys_from_json_str(json_str: str) -> str:
    """Recursively remove the key from a json str and return a json str."""
    try:
        dict_obj = json.loads(json_str)
        remove_blacklisted_logging_keys_from_dict(dict_obj)
        return json.dumps(dict_obj)
    except Exception:
        # Delete the whole string since it cannot be parsed properly
        return "***Information Scrubbed For Logging Purposes***"


def log_system_info(logger: logging.Logger, prefix_message: str = '') -> None:
    """
    Log cpu, memory and OS info.

    :param logger: logger object
    :param prefix_message: string that in the prefix in the log
    :return: None
    """
    if prefix_message is None:
        prefix_message = ''

    try:
        import psutil

        cpu_count, logical_cpu_count = psutil.cpu_count(logical=False), psutil.cpu_count()
        virtual_memory, swap_memory = psutil.virtual_memory().total, psutil.swap_memory().total
        extra_info = {
            'properties': {
                'CPUCount': cpu_count,
                'LogicalCPUCount': logical_cpu_count,
                'VirtualMemory': virtual_memory,
                'SwapMemory': swap_memory
            }
        }
        logger.info("{}CPU logical cores: {}, CPU cores: {}, virtual memory: {}, swap memory: {}.".format(
            prefix_message, logical_cpu_count, cpu_count, virtual_memory, swap_memory), extra=extra_info)
    except Exception:
        logger.warning("Failed to log system info using psutil.")

    import platform
    logger.info("{}Platform information: {}.".format(prefix_message, platform.system()))


def _found_handler(logger: logging.Logger, handle_name: Any) -> bool:
    """
    Check logger with the given handler and return the found status.

    :param logger: Logger
    :param handle_name: handler name
    :return: boolean: True if found else False
    """
    for log_handler in logger.handlers:
        if isinstance(log_handler, handle_name):
            return True

    return False


@contextlib.contextmanager
def log_activity(logger: Optional[Union[logging.Logger, logging.LoggerAdapter]],
                 activity_name: str = '',
                 activity_type: str = '',
                 custom_dimensions: Dict[str, Any] = {}) -> Any:
    """
    Log the activity status with duration.

    :param logger: logger
    :param activity_name: activity name
    :param activity_type: activity type
    :param custom_dimensions: custom dimensions
    """
    # In case logger is None, get the default logger.
    if logger is None:
        logger = logging.getLogger()

    activity_info = dict(activity_id=str(uuid.uuid4()), activity_name=activity_name, activity_type=activity_type) \
        # type: Dict[str, Union[str, float]]

    properties = dict()
    activity_info.update(custom_dimensions)
    properties['properties'] = activity_info

    completion_status = TelemetryConstants.SUCCESS

    start_time = datetime.utcnow()
    logger.info("ActivityStarted: {}".format(activity_name), extra=properties)

    try:
        yield
    except Exception:
        completion_status = TelemetryConstants.FAILURE
        raise
    finally:
        end_time = datetime.utcnow()
        duration_ms = round((end_time - start_time).total_seconds() * 1000, 2)
        activity_info["durationMs"] = duration_ms
        activity_info["completionStatus"] = completion_status

        logger.info("ActivityCompleted: Activity={}, HowEnded={}, Duration={}[ms]".
                    format(activity_name, completion_status, duration_ms), extra=properties)


class LogConfig:
    """
    Class containing the information needed to create a new logger.

    The Python logger is not serializable, so passing this data is sufficient to recreate a logger in a subprocess
    where all arguments must be serializable.
    """

    def __init__(self, log_filename: Optional[str], log_verbosity: int, log_namespace: str) -> None:
        """
        Construct a LogConfig object.

        :param log_filename: name of the log file
        :param log_verbosity: the logging verbosity level
        :param log_namespace: the logging namespace
        """
        self._log_filename = log_filename
        self._log_verbosity = log_verbosity
        self._log_namespace = log_namespace
        self._custom_dimensions = {'app_name': DEFAULT_LOGGING_APP_NAME}

    def get_params(self) -> Tuple[Optional[str], int, str]:
        """Get the logging params."""
        return self._log_filename, self._log_verbosity, self._log_namespace

    def get_filename(self) -> Optional[str]:
        """Get the log filename."""
        return self._log_filename

    def get_namespace(self) -> str:
        """Get the log namespace."""
        return self._log_namespace

    def get_verbosity(self) -> int:
        """Get the log verbosity."""
        return self._log_verbosity

    def get_component_name(self) -> str:
        """Get the component name."""
        return TelemetryConstants.COMPONENT_NAME

    def get_custom_dimensions(self) -> Dict[str, Any]:
        """Get the custom dimensions."""
        return self._custom_dimensions

    def set_custom_dimensions(self, custom_dimensions: Dict[str, Any]) -> None:
        """
        Set the custom dimensions according to existing loggers.

        :param custom_dimensions: Custom dimensions to be added to the log.
        """
        self._custom_dimensions.update(custom_dimensions)

    @classmethod
    def from_logger(cls, logger: Union[logging.Logger, logging.LoggerAdapter]) -> 'LogConfig':
        if isinstance(logger, logging.Logger):
            actual_logger = logger
        else:
            actual_logger = logger.logger

        verbosity = actual_logger.getEffectiveLevel()
        namespace = actual_logger.name
        filename = None
        # Can't reference directly due to circular import
        custom_dimensions = getattr(logger, 'custom_dimensions', {})
        for handler in actual_logger.handlers:
            if isinstance(handler, logging.FileHandler):
                filename = handler.baseFilename
                break
        ret = cls(filename, verbosity, namespace)
        ret.set_custom_dimensions(custom_dimensions)
        return ret


class _CustomStackSummary(traceback.StackSummary):
    """Subclass of StackSummary."""

    def format(self: traceback.StackSummary) -> List[str]:
        """Format the stack ready for printing.

        Returns a list of strings ready for printing.  Each string in the
        resulting list corresponds to a single frame from the stack.
        Each string ends in a newline; the strings may contain internal
        newlines as well, for those items with source text lines.
        """
        result = []
        for frame in self:
            row = ['  File "{}", line {}, in {}\n'.format(
                os.path.basename(frame.filename), frame.lineno, frame.name)]
            if frame.line:
                row.append('    {}\n'.format(frame.line.strip()))
            if frame.locals:
                for name, value in sorted(frame.locals.items()):
                    row.append('    {name} = {value}\n'.format(name=name, value=value))
            result.append(''.join(row))
        return result

    def format_whitelisted_paths(self: traceback.StackSummary) -> List[str]:
        """Format the traceback, removing any unwhitelisted paths."""
        result = []
        for frame in self:
            path = os.path.dirname(frame.filename)
            if is_path_whitelisted(path):
                row = ['  File "{}", line {}, in {}\n'.format(
                    os.path.basename(frame.filename), frame.lineno, frame.name)]
                if frame.line:
                    row.append('    {}\n'.format(frame.line.strip()))
                if frame.locals:
                    for name, value in sorted(frame.locals.items()):
                        row.append('    {name} = {value}\n'.format(name=name, value=value))
            else:
                row = ['  File "{}", line {}, in {}\n'.format(
                    '[Non-AutoML file]', frame.lineno, '[Non-AutoML function]')]
            result.append(''.join(row))
        return result

    @staticmethod
    def get_traceback_message(traceback_obj: Any, remove_pii: bool = True) -> str:
        traceback_not_available_msg = 'Not available (exception was not raised but was returned directly)'
        if traceback_obj is None:
            return traceback_not_available_msg

        if is_exception_stacktrace_loggable() or not remove_pii:
            return ''.join(_CustomStackSummary.format(traceback.extract_tb(traceback_obj)))

        return ''.join(_CustomStackSummary.format_whitelisted_paths(traceback.extract_tb(traceback_obj)))
