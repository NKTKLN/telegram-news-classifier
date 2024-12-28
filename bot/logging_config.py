import logging


def setup_logger() -> None:
    """
    Sets up the logger with a specific format and stream handler to display logs to the console.

    :returns: None
    """
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logger = logging.getLogger()  # Get the root logger
    logger.setLevel(logging.INFO)  # Set the log level to INFO

    # Create a stream handler to output logs to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Set the handler log level to INFO
    console_handler.setFormatter(logging.Formatter(log_format))  # Apply the formatter to the handler

    # Add the handler to the logger
    logger.addHandler(console_handler)

    # Log that the logger setup is complete
    logger.info("Logger setup complete.")
