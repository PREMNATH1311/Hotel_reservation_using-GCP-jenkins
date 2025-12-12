import os
import sys
import yaml
import pandas
from src.logger import logging
from src.custom_expception import CustomException
import pandas as pd

logger=logging.getLogger(__name__)


def read_yaml(file):
    """Reads a YAML file and returns its contents as a dictionary.

    Args:
        file (str): Path to the YAML file.

    Returns:
        dict: The contents of the YAML file as a dictionary.
    """
    try:
        if not os.path.exists(file):
            raise FileNotFoundError(f"yaml file: {file} does not exist")
        with open(file, "rb") as yaml_file:
            config= yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {file} loaded successfully")
            return config
    except Exception as e:
        logger.error(f"Error occurred while reading yaml file: {file} \n{e}")
        raise CustomException("Failed to read yaml file",e) from e
    
def load_data(file_path):
    """Loads data from a CSV file into a pandas DataFrame.

    Args:
        file_path (str): Path to the CSV file."""
    try:
            logger.info(f"Loading data from file: {file_path}")
            return pd.read_csv(file_path)
    
    except Exception as e:
            logger.error(f"Error occurred while loading data from file: {file_path} \n{e}")
            raise CustomException("Failed to load data",e) from e