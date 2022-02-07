import pandas as pd
import pickle
import requests
from flask import Flask, request, Response
from rossman.Rossman import Rossman


# Importing model
model = pickle.load(open('/home/pedro/Documentos/repositories/1-Rossman-Sales-Prediction/model/model_xgb_tuned.pkl','rb'))

# Initialize API
app = Flask(__name__)

@app.route('/rossman/predict', methods=['POST'])

def rossman_predict():
    
    test_json = request.get_json()
    
    if test_json:
        
        if isinstance(test_json, dict): # Unique Example
        
            test_raw = pd.DataFrame(test_json, index=[0])
        
        else: # Multiple Examples
        
            test_raw = pd.DataFrame(test_json, columns=test_json[0].keys())
            
        # Instantiate Rossman class
        
        pipeline = Rossman()
        
        # Data cleaning
        df1 = pipeline.data_cleaning(test_raw)
        # Feature engineering
        df2 = pipeline.feature_engineering(df1)
        # Data preparation
        df3 = pipeline.data_preparation(df2)
        # Prediction
        df_response = pipeline.get_prediction(model, test_raw, df3)
        
        return df_response
        
    else:
        return Response('{}', status=200, mimetype='application/json')
    
if __name__ == '__main__':
    
    app.run('0.0.0.0')
