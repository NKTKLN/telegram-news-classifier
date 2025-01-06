import logging


def setup_logger(log_level: int = logging.INFO) -> None:
    """
    Sets up the logger to display logs to the console.

    :param log_level: The logging level. Default is logging.INFO.
    """
    # Setting the log format for better readability
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configuring the logging settings
    logging.basicConfig(level=log_level, format=log_format)
    
    # Getting the logger instance
    logger = logging.getLogger(__name__)
    
    # Log a message indicating the logger setup completion
    logger.info("Logger setup complete.")
