import logging

DEFAULT_LOG_FMT = '%(asctime)s %(name)-20s %(levelname)-3s : %(message)s'


def setup_logging(verbosity='info', filename=None,
                  log_fmt=DEFAULT_LOG_FMT) -> None:
    """
    Create a basic configuration for the logging library. Set up console and file handler using provided `log_fmt`.
    :param verbosity: verbosity to use, info by default
    :param filename: where to store the log file
    :param log_fmt: format string for logging
    :return: None
    """
    # TODO - find out how to log to file only if filename is specified
    level = parse_logging_level(verbosity)
    # create logger
    logger = logging.getLogger()
    logger.setLevel(level)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(level)
    # create formatter
    formatter = logging.Formatter(log_fmt)
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)


def parse_logging_level(verbosity: str) -> int:
    """Parse logging verbosity level
    :param verbosity: string representing verbosity, recoginzed strings are {debug, info, warning, error, critical}
    :return: verbosity level as integer
    """
    vu = verbosity.lower()
    if vu == "debug":
        return logging.DEBUG
    elif vu == "info":
        return logging.INFO
    elif vu == "warning":
        return logging.WARNING
    elif vu == "error":
        return logging.ERROR
    elif vu == "critical":
        return logging.CRITICAL
    else:
        print("Unknown logging level {}".format(verbosity))
        return logging.INFO
