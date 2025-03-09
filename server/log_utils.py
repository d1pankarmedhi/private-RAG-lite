from loguru import logger

LOG_FILE_NAME = "app.log"
LOG_ROTATION_SIZE = "1 MB"
LOG_LEVEL_CONSOLE = "INFO"
LOG_LEVEL_FILE = "DEBUG"


def get_logger():
    """Configures logger for console and file logger with rotation."""

    logger.remove()  # Remove default sink
    logger.add(
        LOG_FILE_NAME,
        rotation=LOG_ROTATION_SIZE,
        level=LOG_LEVEL_FILE,
        enqueue=True,
        backtrace=False,
        diagnose=False,
    )
    logger.info("logger system initialized.")


get_logger()

__all__ = ["logger"]
