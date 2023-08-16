import os
import sys

import numpy as np 
import pandas as pd
import dill
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)
    
def categorize_job_title(job_title):
        job_title = str(job_title).lower()
        if "software" in job_title or "developer" in job_title:
            return 'Software/Developer'
        elif "data" in job_title or 'analyst' in job_title or 'scientist' in job_title:
            return 'Data Analyst/Scientist'
        elif "sales" in job_title or "reprentative" in job_title:
            return 'Sales'
        elif 'manager' in job_title or 'director' in job_title or 'vp' in job_title:
            return 'Manager/Director/vp'
        elif 'marketing' in job_title or 'social media' in job_title:
            return 'Marketing/Social Media'
        elif 'product' in job_title or 'designer' in job_title:
            return 'Product/Designer'
        elif 'hr' in job_title or 'human resource' in job_title:
            return 'HR/Human Resource'
        elif 'financial' in job_title or 'accountant' in job_title:
            return 'Financial/Accountant'
        elif 'project manager' in job_title:
            return 'Project Manager'
        elif 'it' in job_title or 'support' in job_title:
            return 'IT/Technical Support'
        elif 'operations' in job_title or 'supply chain' in job_title:
            return  'Operations/Supply Chain'
        elif 'customer service' in job_title or 'receptionalist' in job_title:
            return 'Customer Service/Receptionalist'
        else:
            return "Other"
        
def evaluate_models(X_train, y_train,X_test,y_test,models,param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para=param[list(models.keys())[i]]

            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)

            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report
    except Exception as e:
        raise CustomException(e,sys)

def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys)