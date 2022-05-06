import logging
import inspect

class ApplicationLogging:
    def __init__(self):
        self.loggerName = inspect.stack()[1][1]
        self.logger = logging.getLogger(self.loggerName)
        self.logger.setLevel(logging.DEBUG)
        self.fileHandler = logging.FileHandler("logging_details/logRecord.log", mode='a')
        self.formatter = logging.Formatter('%(asctime)s  [%(levelname)s] - %(name)s :: %(message)s', datefmt='%d/%m/%Y  %I:%M:%S %p')
        self.fileHandler.setFormatter(self.formatter)
        self.logger.addHandler(self.fileHandler)

    def Debug(self, message):
        self.logger.debug(message)

    def Info(self, message):
        self.logger.info(message)

    def Warning(self, message):
        self.logger.warning(message)

    def Error(self, message):
        self.logger.error(message)

    def Critical(self, message):
        self.logger.critical(message)