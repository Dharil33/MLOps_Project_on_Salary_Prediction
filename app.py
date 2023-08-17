from flask import Flask,request,render_template
import numpy as np
import pandas as pd
import sys
from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData,PredictPipeline
from src.logger import logging
from src.exception import CustomException


application = Flask(__name__)

app = application

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictdata',methods=['GET','POST'])
def predict_salary():
    try:
        if request.method == 'GET':
            return render_template('home.html')
        else:
            data = CustomData(
                Gender=request.form.get('Gender'),
                Education_Level=request.form.get('Education_Level'),
                Age=request.form.get('Age'),
                Job_Title=request.form.get('Job_Title'),
                Years_of_Experience=request.form.get('Years_of_Experience'),
            )
            pred_df = data.get_data_as_dataframe()
            print(pred_df)
            logging.info("Before the prediction")
            predictpipeline_obj = PredictPipeline()
            results = predictpipeline_obj.predict(pred_df)
            logging.info("After the prediction")
            return render_template('home.html',results=int(results[0]))
    except Exception as e:
        raise CustomException(e,sys)
        
if __name__== '__main__':
    app.run(host='0.0.0.0',port=8080)
