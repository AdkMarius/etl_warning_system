import logging
from datetime import datetime, timedelta
import os


def setup_logging(log_level=logging.INFO):
    """
    Set up basic logging configuration.

    Parameters:
    - log_level: The root logger level (default is logging.INFO).
    """
    # Define the directory for log files
    log_dir = "logs"

    # Ensure the directory exists
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Generate the filenames for today and yesterday's logs
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_filename_today = os.path.join(log_dir, f"log_{current_date}.log")
    log_filename_yesterday = os.path.join(log_dir,
                                          f"log_{(datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')}.log")

    # Remove yesterday's log file if it exists
    if os.path.exists(log_filename_yesterday):
        os.remove(log_filename_yesterday)

    # Set up the basic configuration for logging
    logging.basicConfig(
        filename=log_filename_today,
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
