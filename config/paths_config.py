import os

###### Data Ingestion Configurations ######
RAW_DIR="artifacts/raw"
RAW_FILE_PATH=os.path.join(RAW_DIR,"raw.csv")
TRAIN_FILE_PATH=os.path.join(RAW_DIR,"train.csv")
TEST_FILE_PATH=os.path.join(RAW_DIR,"test.csv")

CONFIG_PATH="config/config.yaml"

###### Data Transformation Configurations ######
TRANSFORMED_DIR="artifacts/transformed"


### Data processing Configurations ###
PROCESSED_DIR="artifacts/processed"
PROCESSED_TRAIN_FILE_PATH=os.path.join(PROCESSED_DIR,"processed_train.csv")
PROCESSED_TEST_FILE_PATH=os.path.join(PROCESSED_DIR,"processed_test.csv")


####### model training###

LOCAL_MODEL_PATH = "artifacts/model/lgbm_model.pkl"
GCS_MODEL_PATH = "gs://hotel-ml-models/lgbm_model.pkl"

MODEL_OUTPUT_PATH = (
    GCS_MODEL_PATH
    if os.getenv("CLOUD_RUN") == "true"
    else LOCAL_MODEL_PATH
)


