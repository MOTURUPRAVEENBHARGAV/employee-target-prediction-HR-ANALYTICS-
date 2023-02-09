from datetime import datetime as dt
from flask import Flask,redirect, url_for, render_template,request,jsonify
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier,GradientBoostingClassifier
from joblib import load, dump
import warnings
warnings.filterwarnings("ignore")
import json
from flask_cors import CORS
from flask_ngrok import run_with_ngrok

#load the MODEL 
KNN= load("KNeighborsClassifier.pkl")
# GDB= pickle.load(open("GradientboostClassifier.pkl","rb"))
  #Scaler
scaler=load("model_scaler.pkl")

#WSGI Application
app= application =  Flask(__name__) #Flask App Object
@app.route('/') #Home Page
def welcome():
    return "Welcome"

@app.route('/predict',methods=['POST', 'GET'])
def pop_results():
    # global record
    # record=dict()
    if request.method == "POST":

        data = request.data
        # json_data= data.content
        json_data= json.loads(data)
        print(json_data)
        record={}
        
        # for key,value in json_data.items():
        #     # l.append(value)
        #     record[key]=value
        
        

        # json_data = {
        #             "createdAt":"2023-02-05T18:20:00",
        #             "updatedAt":"2023-02-06T18:20:00",
        #             "progress":"80",
        #             "targetDate":"2023-02-07T23:59:59"
        #             }

        cr_date= json_data["createdAt"].split("T")[0]
        cr_date= dt.strptime(cr_date,"%Y-%m-%d")


        up_date= json_data["updatedAt"].split("T")[0]
        up_date= dt.strptime(up_date,"%Y-%m-%d")

        act_work = json_data["progress"]

        trg_date= json_data["targetDate"].split("T")[0]
        trg_date= dt.strptime(trg_date,"%Y-%m-%d")

        Target_Days = trg_date - cr_date
        Target_Days = Target_Days.days #1st Attribute

        Actual_Days =  up_date - cr_date
        Actual_Days= Actual_Days.days#2nd Attribute

        Remaining_Days = Target_Days - Actual_Days #3rd Attribute

        Actual_Work = int(json_data["progress"])/100  #4th Attribute
        Remaining_Work = 1 - Actual_Work #5th Attribute

        #typecast into array
        test_data = np.array([Target_Days, Actual_Days, Remaining_Days, Actual_Work, Remaining_Work]).reshape(1,-1)

        
        scale_data = scaler.transform(test_data)

        #Load the model
         

        probability =KNN.predict_proba(scale_data)[0][1]

        #copy the dictionary
        record = json_data.copy()
    

        record["probability"] = str(round(probability*100,2)) + "%"
    # print(data)

    return record



if __name__ == '__main__':
    app.run(debug = True)