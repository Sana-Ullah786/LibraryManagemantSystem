import logging
import os
from datetime import datetime


def get_current_date() -> str:
    """
    This function returns the current date in the format mm-dd-yyyy
    Parameters:
        None
    Returns:
        str: Current date in the format mm-dd-yyyy
    """
    return datetime.now().strftime("%m-%d-%Y")


def check_file_exits(file_name: str) -> bool:
    """
    This function checks if the file exists
    Parameters:
        file_name (str): Name of the file
    Returns:
        bool: True if the file exists, False otherwise
    """
    return os.path.exists(file_name)


def setup_logging() -> None:
    """
    This function sets up the logging for the program
    Parameters:
        None
    Returns:
        None
    """
    directory = "logs"
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_name = os.path.join(directory, get_current_date() + ".log")
    if check_file_exits(file_name):
        logging.basicConfig(
            filename=file_name,
            filemode="a",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s: %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S %p",
        )
    else:
        logging.basicConfig(
            filename=file_name,
            filemode="w",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s: %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S %p",
        )
