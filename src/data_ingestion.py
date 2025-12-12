import os
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import logging
from src.custom_expception import CustomException
import sys
from config.paths_config import *
from utils.common_functions import read_yaml

logger=logging.getLogger(__name__)

class DataIngestion:
    def __init__(self, config_path):
        self.config = read_yaml(config_path)["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.bucket_file_name = self.config["bucket_file_name"]
        self.train_ratio = self.config["train_ratio"]
        
        os.makedirs(RAW_DIR, exist_ok=True)
        logger.info(f"Data Ingestion stated with bucket: {self.bucket_name}, file: {self.bucket_file_name}, train_ratio: {self.train_ratio}")

    def download_data(self):
        """Downloads data from Google Cloud Storage bucket."""
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.bucket_file_name)
            blob.download_to_filename(RAW_FILE_PATH)
            logger.info(f"Data downloaded from bucket {self.bucket_name} to {RAW_FILE_PATH}")
        except Exception as e:
            logger.error(f"Error occurred while downloading data: {e}")
            raise CustomException("Failed to download data from GCS", e) from e

    def split_data(self):
        """Splits the data into training and testing sets."""
        try:
            df = pd.read_csv(RAW_FILE_PATH)
            train_data, test_data = train_test_split(df, test_size=1-self.train_ratio, random_state=42)
            train_data.to_csv(TRAIN_FILE_PATH, index=False)
            test_data.to_csv(TEST_FILE_PATH, index=False)
            logger.info(f"Data split into train and test sets at {TRAIN_FILE_PATH} and {TEST_FILE_PATH}")
        except Exception as e:
            logger.error(f"Error occurred while splitting data: {e}")
            raise CustomException("Failed to split data", e) from e

    def initiate_data_ingestion(self):
        """Initiates the data ingestion process."""
        try:
            logger.info("Initiating data ingestion")
            self.download_data()
            self.split_data()
            logger.info("Data ingestion completed successfully")
            
        except CustomException as e:
            logger.error(f"Error occurred during data ingestion: {e}")
            raise CustomException("Data ingestion failed", e) from e
        finally:
            logger.info("Data Ingestion process finished")
            
if __name__ == "__main__":
    data_ingestion = DataIngestion(CONFIG_PATH)
    data_ingestion.initiate_data_ingestion()