import os
import pandas as pd
import joblib
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score
from src.logger import get_logger
from src.custom_expception import CustomException
from config.paths_config import *
from config.model_params import *
from utils.common_functions import read_yaml,load_data
from scipy.stats import randint
from sklearn.model_selection import train_test_split
import mlflow
import mlflow.sklearn

logger=get_logger(__name__)


class ModelTraining:
    def __init__(self,train_path,test_path,model_output_path):
        
        self.train_path=train_path
        self.test_path=test_path
        self.model_output_path=model_output_path
        
        
        self.params_dist=LIGHTGM_PARAMS
        self.random_serach_params=RANDOM_SEARCH_PARAMS
        
    def load_and_split_data(self):
        try:
            logger.info(f"Loading the data from {self.train_path}")
            train_df=load_data(self.train_path)
            
            logger.info(f"Loading data from {self.test_path}")
            test_df=load_data(self.test_path)
            
            X_train=train_df.drop(columns=['booking_status'])
            y_train=train_df['booking_status']
            
            X_test=test_df.drop(columns=['booking_status'])
            y_test=test_df['booking_status']
            
            logger.info("Data splitted sucessfully for Model Training")
            
            return X_train,y_train,X_test,y_test
        
        except Exception as e:
            logger.error("Error while loading data {e}")
            raise CustomException("Failed to load data",e)
        
    
    def train_lgbm(self,X_train,y_train):
        try:
            logger.info("Intializing our model")
            
            lgbm_model=lgb.LGBMClassifier(random_state=self.random_serach_params['random_state'])
            
            logger.info("Starting our hyper parameter tuning")
            
            random_search=RandomizedSearchCV(
                estimator=lgbm_model,
                param_distributions=self.params_dist,
                n_iter=self.random_serach_params['n_iter'],
                scoring=self.random_serach_params['scoring'],
                cv=self.random_serach_params['cv'],
                n_jobs=self.random_serach_params['n_jobs'],
                verbose=self.random_serach_params['verbose'],
                random_state=self.random_serach_params['random_state']
                
            )
            
            logger.info("Starting our Hyperparameter tuning")
            
            random_search.fit(X_train,y_train)
            
            logger.info("Hyperparameters tuning completed")
            
            best_params=random_search.best_params_
            best_lgbm_model=random_search.best_estimator_
            
            logger.info(f"Best parameters are : {best_params}")
            
            return best_lgbm_model
        
        except Exception as e:
            logger.error(f"Error while training model {e}")
            raise CustomException("Failed to train model",e)
            
            
    
    def evaluate_model(self,model,X_test,y_test):
        
    
        try:
            logger.info("Evaluating our model")
            
            y_pred=model.predict(X_test)
            
            
            accuracy=accuracy_score(y_test,y_pred)
            precision=precision_score(y_test,y_pred)
            recall=recall_score(y_test,y_pred)
            f1=f1_score(y_test,y_pred)
            
            
            logger.info(f"Accuracy score:{accuracy}")
            logger.info(f"Precision score: {precision}")
            logger.info(f"Recall Score: {recall}")
            logger.info(f"F1 score: {f1}")
            
            return {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'F1': f1
            }        
    
        except Exception as e:
            logger.error(f"Error while evaluating model {e}")    
            raise CustomException("Failed to evaluate Model",e)
     
     
    def save_model(self,model):
        try:
            os.makedirs(os.path.dirname(self.model_output_path),exist_ok=True)
            
            logger.info("Saving the Model")
            
            joblib.dump(model,self.model_output_path)
            
            logger.info(f"Model saved to {self.model_output_path}")
            
            
        except Exception as e:
            logger.error(f"Error while saving model {e}")
            raise CustomException("Failed to Save model",e)
        
        
    def run(self):
        try:
            with mlflow.start_run():
                logger.info("Starting Our Model Training Pipeline")

                # STEP 1 — Load data
                X_train, y_train, X_test, y_test = self.load_and_split_data()

                # STEP 2 — Train model
                best_lgbm_model = self.train_lgbm(X_train, y_train)

                # STEP 3 — Evaluate model
                metrics = self.evaluate_model(best_lgbm_model, X_test, y_test)

                # STEP 4 — Save model
                self.save_model(best_lgbm_model)

                # STEP 5 — MLFLOW LOGGING
                logger.info("Logging artifacts, params and metrics to MLflow")

                # log input datasets
                mlflow.log_artifact(self.train_path, artifact_path="datasets")
                mlflow.log_artifact(self.test_path, artifact_path="datasets")

                # log model params
                mlflow.log_params(best_lgbm_model.get_params())

                # log metrics
                mlflow.log_metrics(metrics)

                # log saved model file
                mlflow.log_artifact(self.model_output_path, artifact_path="models")

                logger.info("Model Training Successfully Completed")

        except Exception as e:
            logger.error(f"Error in model training pipeline {e}")
            raise CustomException("Failed during Model training pipeline", e)

    # def run(self):
    #     try:
    #         with mlflow.start_run():
    #             logger.info("Starting Our Model Training Pipeline")
                
    #             logger.info("starting the MLFLOW experimentation")
                
    #             logger.info("Logging the training and testing dataset to MLFLOW")
                
    #             # storing the dataset in mlflow
    #             mlflow.log_artifact(self.train_path,artifact_path="datasets")
    #             mlflow.log_artifact(self.test_path,artifact_path="datasets")
                
                
    #             logger.info("Logging the model into MLFLOW")
    #             mlflow.log_artifact(self.model_output_path)
                
                
    #             mlflow.log_params(best_lgbm_model.get_params())
                
    #             logger.info("Logging params and metrics to MLFLOW")
    #             #
    #             mlflow.log_metric(metrics)
                
                
                
    #             X_train,y_train,X_test,y_test=self.load_and_split_data()
    #             best_lgbm_model=self.train_lgbm(X_train,y_train)
    #             metrics=self.evaluate_model(best_lgbm_model,X_test,y_test)
    #             self.save_model(best_lgbm_model)
    #             logger.info("Model Training Sucessfully completed")
    #     except Exception as e:
    #         logger.error(f"Error in model training pipeline {e}")
    #         raise CustomException("Failed during Model traiing pipeline",e)
        
if __name__=="__main__":
    trainer=ModelTraining(PROCESSED_TRAIN_FILE_PATH,PROCESSED_TEST_FILE_PATH,MODEL_OUTPUT_PATH)
    trainer.run()
    
            
        
        
        
            
            
            
        
        
        
        
        