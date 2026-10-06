import logging
import os

# Project root
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

# Logs folder
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Exact log file path
LOG_FILE = os.path.join(LOG_DIR, "app.log")

print("LOG FILE:", LOG_FILE)

logger = logging.getLogger("AttendanceAutomation")
logger.setLevel(logging.INFO)
logger.propagate = False

if not logger.handlers:

    file_handler = logging.FileHandler(
        LOG_FILE,
        mode="a",
        encoding="utf-8"
    )

    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

logger.info("Logger initialized successfully.")