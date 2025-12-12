import pandas as pd
import os
import sys
import numpy as np
from src.logger import get_logger
from src.custom_expception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml,load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE


logger=get_logger(__name__)


class DataProcessor:
    def __init__(self,train_path,test_path,processed_dir,config_path):
        self.train_path=train_path
        self.test_path=test_path
        self.processed_dir=processed_dir
        self.config=read_yaml(config_path)
        
        
        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)
            
    def preprocess_data(self,df):
        try:
            logger.info("Starting our Data Processing step")
            
            logger.info("Dropping Unwanted Columns:")
            df.drop(columns=['Booking_ID'],inplace=True)
            
            df.drop_duplicates(inplace=True)
            
            cat_col=self.config['data_processing']['categorial_cols']
            num_col=self.config['data_processing']['numerical_cols']
            
            logger.info("Applying LabelEncoding")
            
            label_encoder = LabelEncoder()
            mapping={}
            for col in cat_col:
                
                df[col] = label_encoder.fit_transform(df[col])
                mapping[col] = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))
            logger.info(f"------Label Mapping started -----")
            
            
            for col,mapping in mapping.items():
                logger.info(f"{col}:{mapping}")
                
            logger.info("Doing Skewness Handling")
            
            skewness_thershold=self.config['data_processing']['skewness_thershold']
            
            skewness=df[num_col].apply(lambda x:x.skew())
            for columns in skewness[skewness>skewness_thershold].index:
                df[columns]=np.log1p(df[columns])
            
            return df
                
        except Exception as e:
            logger.error(f"Error during preprocess Test {e}")
            raise CustomException(f"Error while processes data",e)
        
    def balance_data(self,df):
        try:
            logger.info("Handling Imbalance data")
            X=df.drop(columns='booking_status')
            y=df['booking_status']
            
            smote=SMOTE(random_state=42)
            X_resampled,y_resampled=smote.fit_resample(X,y)
            
            balanced_df=pd.DataFrame(X_resampled,columns=X.columns)
            balanced_df['booking_status']=y_resampled
            
            logger.info("Data balanced sucessfully")
            return balanced_df
        except Exception as e:
            logger.error(f"Error during balancing data step {e}")
            raise CustomException(f"Error while balancing Data",e)
        
        
    def feature_selection(self,df):
        try:
            logger.info("Starting Feature selection step")
            X=df.drop(columns='booking_status')
            y=df['booking_status']
            
            model=RandomForestClassifier(random_state=42)
            model.fit(X,y)
            feature_importance=model.feature_importances_
            feature_importance_df=pd.DataFrame({
                'feature':X.columns,
                'importance': feature_importance
            })
            top_features_importance_df=feature_importance_df.sort_values(by="importance",ascending=False)
            
            num_features_to_select=self.config['data_processing']['no_of_features']
            top_10_features=top_features_importance_df['feature'].head(num_features_to_select).values
            
            logger.info(f"top 10 features selected:{top_10_features}")
            
            top_10_df=df[top_10_features.tolist()+['booking_status']]
            
            logger.info(f"feature selection completed sucessfully")
            
            return top_10_df
        
        except Exception as e:
            logger.error(f"Error during feature selection step {e} ")
            raise CustomException("Error while feature selection",e)
            
            
    def save_data(self,df,file_path):
        try:
            logger.info("saving Our data in processed folder")
            df.to_csv(file_path,index=False)
            
            logger.info(f"data saved sucessfully to {file_path}")
            
        except Exception as e:
            logger.error("Error during saving step {e}")
            raise CustomException("Error while saving data",e)
    
    def process(self):
        try:
            logger.info("Loading the Data from Raw directory")
            train_df=load_data(self.train_path)
            test_df=load_data(self.test_path)
            
            train_df=self.preprocess_data(train_df)
            test_df=self.preprocess_data(test_df)
            
            
            train_df=self.balance_data(train_df)
            # we don't need to balance test df
            test_df=self.balance_data(test_df)
            
            
            
            train_df=self.feature_selection(train_df)
            
            test_df=test_df[train_df.columns]
            
            self.save_data(train_df,PROCESSED_TRAIN_FILE_PATH)
            self.save_data(test_df,PROCESSED_TEST_FILE_PATH)
            
            logger.info("Data Processing completed sucessfully")
            
        except Exception as e:
            logger.info("Error during preprocessing pipeline {e}")
            raise CustomException("Error while data preprocessing pipeline",{e})
            
            
            
if __name__=="__main__":
    processor=DataProcessor(TRAIN_FILE_PATH,TEST_FILE_PATH,PROCESSED_DIR,CONFIG_PATH)
    processor.process()
    
    
            
            
            
            
            
            
                        
            
