from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataProcessor
from src.model_training import ModelTraining
from config.paths_config import *





if __name__=="__main__":
    
    # Data Ingestion
    
    data_ingestion = DataIngestion(CONFIG_PATH)
    data_ingestion.initiate_data_ingestion()
    
    # Data preprocessing
    processor=DataProcessor(TRAIN_FILE_PATH,TEST_FILE_PATH,PROCESSED_DIR,CONFIG_PATH)
    processor.process()
    
    #Model training
    trainer=ModelTraining(PROCESSED_TRAIN_FILE_PATH,PROCESSED_TEST_FILE_PATH,MODEL_OUTPUT_PATH)
    trainer.run()