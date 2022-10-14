import os
import logging

logFormatter = logging.Formatter(
    "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"
)
rootLogger = logging.getLogger()

logPath = os.getenv("logPath", "logs")
fileHandler = logging.FileHandler(f"{logPath}.log")
fileHandler.setFormatter(logFormatter)
fileHandler.setLevel("DEBUG")
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
consoleHandler.setLevel("INFO")
rootLogger.addHandler(consoleHandler)
rootLogger.setLevel("INFO")