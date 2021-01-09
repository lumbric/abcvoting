"""
Print messages to terminal depending on a given verbosity level similar to the Python logging
module. Also meant to be used as Singleton.
"""

CRITICAL = 50
ERROR = 40
WARNING = 30
INFO = 20
DEBUG = 10
DEBUG2 = 5

LEVEL_TO_NAME = {
    CRITICAL: "CRITICAL",
    ERROR: "ERROR",
    WARNING: "WARNING",
    INFO: "INFO",
    DEBUG: "DEBUG",
    DEBUG2: "DEBUG2",
}


class Cout:
    """
    This is inspired by the class ``logging.Logger()``. A verbosity level is stored,
    only messages printed with methods with higher importance will be printed.
    """

    def __init__(self, level=WARNING, logger=None):
        """At them moment only one instance will created: in the global scope of this module. An
        application might use the `setup()` method to set the level and a logger.

        Parameters
        ----------
        level : int
             verbosity level: minimum level of importance of messages to be printed, as defined by
             constants in this module
        logger : logging.Logger
             can be used to send messages also to a log file or elsewhere

        """
        self.level = level
        self.logger = logger

    def setup(self, level, logger=None):
        self.level = level
        self.logger = logger

    def _print(self, msg_level, msg):
        if msg_level >= self.level:
            print(msg)

        if self.logger:
            if msg_level == DEBUG2:
                log_function = self.logger.debug
            else:
                log_function = getattr(self.logger, LEVEL_TO_NAME[msg_level])
            log_function(msg)

    def debug2(self, msg):
        # this is the old verbose >= 3
        self._print(DEBUG2, msg)

    def debug(self, msg):
        # this is the old verbose >= 2
        self._print(DEBUG, msg)

    def info(self, msg):
        # this is the old verbose >= 1
        self._print(INFO, msg)

    def warning(self, msg):
        # this is the old verbose >= 0
        self._print(WARNING, msg)

    def error(self, msg):
        # to print errors, probably not used atm
        self._print(ERROR, msg)

    def critical(self, msg):
        # just for consistency with the logging module
        self._print(CRITICAL, msg)


cout = Cout()
