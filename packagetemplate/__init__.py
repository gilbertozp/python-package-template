"""
BSD 3-Clause License

Copyright (c) 2017, Gilberto Pastorello
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Template with basic functionality for new Python projects: main package

@author: Gilberto Pastorello
@contact: gzpastorello@lbl.gov
@date: 2017-07-12
"""
import sys
import logging
import traceback

# get logger for this module
_log = logging.getLogger(__name__)

# 'no-op' handler in case no logging setup is done
_log.addHandler(logging.NullHandler())

# logging default formats
LOG_DATEFMT = "%Y-%m-%d %H:%M:%S"
LOG_FMT = "%(asctime)s.%(msecs)03d [%(levelname)-8s] %(message)s [%(name)s]"


class TemplateModuleError(Exception):
    """
    Base error/exception class for TemplateModule
    """


def log_config(level=logging.DEBUG,
               filename=None, filename_level=None,
               std=True, std_level=None,
               log_fmt=LOG_FMT, log_datefmt=LOG_DATEFMT):
    """
    Setup root logger and handlers for log file and STDOUT

    :param level: logging level (from logging library)
    :type level: int
    :param filename: name of log file
    :type filename: str
    :param filename_level: logging level for file log (same as level if None)
    :type filename_level: int
    :param std: if True, sys.stderr will show log messages
    :type std: boolean
    :param std_level: logging level for std log (same as level if None)
    :type std_level: int
    :param log_fmt: log output formatting
    :type log_fmt: str
    :param log_datefmt: log date-time output formatting
    :type log_datefmt: str
    """

    # check and reset log levels
    reset_level = False
    if not isinstance(level, int):
        level = logging.DEBUG
        reset_level = True

    reset_filename_level = False
    if not isinstance(filename_level, int):
        filename_level = level
        reset_filename_level = True

    reset_std_level = False
    if not isinstance(std_level, int):
        std_level = level
        reset_std_level = True

    # setup root logger
    logger_root = logging.getLogger()
    logger_root.setLevel(level)

    # setup formatter
    formatter = logging.Formatter(fmt=log_fmt, datefmt=log_datefmt)

    # setup file handler
    if filename is not None:
        handler_file = logging.FileHandler(filename)
        handler_file.setLevel(filename_level)
        handler_file.setFormatter(formatter)
        logger_root.addHandler(handler_file)

    # setup std handler
    if std:
        handler_console = logging.StreamHandler()
        handler_console.setLevel(level)
        handler_console.setFormatter(formatter)
        logger_root.addHandler(handler_console)

    # initialization message
    logger_root.info("Logging started")

    # registers results from housekeeping checks
    if reset_level:
        logger_root.warn("Invalid logging level, reset to DEBUG")
    if reset_filename_level:
        logger_root.warn("Invalid file logging level, reset to DEBUG")
    if reset_std_level:
        logger_root.warn("Invalid std logging level, reset to DEBUG")
    if filename is None:
        logger_root.info("No log file will be saved")
    if not std:
        logger_root.info("No log entries shown on console")


def log_trace(exception, level=logging.ERROR, log=_log, output_fmt='std'):
    """
    Logs exception including stack traceback into log,
    formatting trace as single line

    :param exception: exception object to be handled
    :type exception: Exception
    :param level: logging severity level
    :type level: int
    :param log: logger to use for logging trace
    :type log: logging.Logger
    :param output_fmt: output format: std (like Python traceback) or
                                      alt (';'-separated single line)
    :type output_fmt: str

    >>> # N.B.: careful when catching Exception class,
    >>> #       this can mask virtually any error in Python
    >>> try:
    >>>     raise Exception('Test exception')
    >>> except Exception as e:
    >>>     msg = log_trace(exception=e, level=logging.CRITICAL)
    >>>     sys.exit(msg)
    """

    # check logger parameter
    if not isinstance(log, logging.Logger):
        # get this function name
        func_name = sys._getframe().f_code.co_name
        msg = "{n} expected <class 'logging.Logger'> object, got {t} instead; using default".format(n=func_name,
                                                                                                    t=type(log))
        log = _log
        log.error(msg)

    # protect trace retrieval
    try:
        # get exc_type, exc_value, exc_traceback
        _, _, exc_traceback = sys.exc_info()
        # format trace
        if output_fmt == 'std':
            # use standard Python formatting (log list, return str)
            message = traceback.format_exception(exception.__class__, exception, exc_traceback)
            log.log(level=level, msg=message)
            message = ''.join(message)
        elif output_fmt == 'alt':
            trace = traceback.extract_tb(exc_traceback)
            message = "Trace for '{e}': ".format(e=str(exception))
            # go through all stack entries
            for t in trace:
                # items are: (filename, line number, function name, text)
                message += "{f}:{p}:{n} '{c}'; ".format(f=t[0], n=t[1], p=t[2], c=t[3])
            log.log(level=level, msg=message)

    # error while trying to retrieve/format trace
    except Exception as e:
        message = "Trace not generated for: '{x}'; ERROR: '{r}'".format(x=str(exception), r=str(e))
        log.error(message)

    # clean-up trace retrieval
    finally:
        # avoid circular reference, per docs
        del exc_traceback

    return message