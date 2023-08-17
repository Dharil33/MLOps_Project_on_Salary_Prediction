import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
import os
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler,LabelEncoder
from src.exception import CustomException
from src.logger import logging
from src.utils.common import save_object,categorize_job_title

@dataclass
class DataTranformationConfig:
    preprocessor_object_file_path = os.path.join('artifacts','preprocessor.pkl')
    
class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTranformationConfig()
      
    def get_transformation_obj(self):
        try:
            cat_features = ['Gender','Education_Level','Job_Title']
            num_features = ['Age','Years_of_Experience']
            
            num_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy='median')),
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )
            cat_pipeline=Pipeline(

                steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ('one_hot_encoder',OneHotEncoder(sparse_output=False,handle_unknown='ignore'))
                ]
            )
            preprocessor=ColumnTransformer(
                [
                ("num_pipeline",num_pipeline,num_features),
                ("cat_pipelines",cat_pipeline,cat_features)
                ]
            )
            return preprocessor
            
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            
            logging.info("Read train and test data completed")
            logging.info("Obtaining preprocessing object")
            
            preprocessing_obj = self.get_transformation_obj()
            target_column_name = "Salary"
            
            train_df.rename(columns={'Years of Experience':'Years_of_Experience',
                                    'Education Level':'Education_Level',
                                    'Job Title':'Job_Title'},inplace=True)
            
            test_df.rename(columns={'Years of Experience':'Years_of_Experience',
                                    'Education Level':'Education_Level',
                                    'Job Title':'Job_Title'},inplace=True)
            
            logging.info(f"train_df: {train_df.columns}")
            logging.info(f"test_df: {test_df.columns}")
            
            train_df.dropna(axis=0,inplace=True)
            test_df.dropna(axis=0,inplace=True)
            
            logging.info("Null values has been removed!!")
            
            train_df['Job_Title'] = train_df['Job_Title'].apply(categorize_job_title)
            test_df['Job_Title'] = test_df['Job_Title'].apply(categorize_job_title)

            logging.info("Job Title has been categorized!!")

            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )            
            
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            target_train_temp_arr = np.array(target_feature_train_df)
            
            train_arr = np.c_[
                input_feature_train_arr, target_train_temp_arr
            ]

            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")

            save_object(

                file_path=self.data_transformation_config.preprocessor_object_file_path,
                obj=preprocessing_obj

            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_object_file_path,
            )
            
        except Exception as e:
            raise CustomException(e,sys)
        
