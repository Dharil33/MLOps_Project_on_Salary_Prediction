import sys
import pandas as pd
from src.exception import CustomException
from src.utils.common import load_object

class PredictPipeline:
    def __init__(self):
        pass

    def predict(self,features):
        try:
            model_path = 'artifacts/model.pkl'
            preprocessor_path = 'artifacts/preprocessor.pkl'
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            return preds
        except Exception as e:
            raise CustomException(e,sys)
        
class CustomData:
    def __init__(self,
                 Gender:str,
                 Education_Level: str,
                 Age: int,
                 Job_Title: str,
                 Years_of_Experience: int,	
    ):
        self.Gender = Gender
        self.Education_Level =Education_Level
        self.Age = Age
        self.Job_Title = Job_Title
        self.Years_of_Experience =Years_of_Experience

    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                "Gender": [self.Gender],
                "Education_Level": [self.Education_Level],
                "Age": [self.Age],
                "Job_Title": [self.Job_Title],
                "Years_of_Experience": [self.Years_of_Experience]
            }
            return pd.DataFrame(custom_data_input_dict)
        except Exception as e:
            raise CustomException(e,sys)