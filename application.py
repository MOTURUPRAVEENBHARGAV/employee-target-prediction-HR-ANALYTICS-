from flask import Flask, render_template, request
import requests
import pickle
import numpy as np
# from datetime import datetime
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
# import pymongo
# from pymongo import MongoClient
import pytz
# import json



application = Flask(__name__)

#load the MODEL 
KNN= load("KNeighborsClassifier.pkl")
# GDB= pickle.load(open("GradientboostClassifier.pkl","rb"))
  #Scaler
scaler=load("model_scaler.pkl")

@application.route('/', methods=['GET'])
# E:\DESKT\INTERNSHIPS\Talent Spotify\ML\model\randomforest_model (2).pkl
def Home():
    return render_template('index.html')


@application.route('/predict',methods=['POST'])
def predict():

    if request.method == 'POST':
        
        global result,now,probability,data

        data=[]
       
        probability = [] 

        createdat= str(request.form["createdat"])
        createdat= dt.strptime(createdat,"%Y-%m-%d").date()
        data.append(createdat.strftime("%d-%m-%Y"))


        targetdate= str(request.form["targetdate"])
        targetdate= dt.strptime(targetdate,"%Y-%m-%d").date()
        data.append(targetdate.strftime("%d-%m-%Y"))


        updatedat= str(request.form["updatedat"])
        updatedat= dt.strptime(updatedat,"%Y-%m-%d").date()
        
        data.append(updatedat.strftime("%d-%m-%Y"))

        progress= int(request.form["progress"])
        data.append(progress)

        Target_Days = targetdate - createdat
        Target_Days = Target_Days.days #1st Attribute  
        data.append(Target_Days)  

        Actual_Days =  updatedat - createdat
        Actual_Days= Actual_Days.days#2nd Attribute
        data.append(Actual_Days)

        Remaining_Days = Target_Days - Actual_Days #3rd Attribute
        data.append(Remaining_Days)

        Actual_Work = int(progress)/100  #4th Attribute

        Remaining_Work = round(1 - Actual_Work,2) #5th Attribute
        data.append(Remaining_Work)

        #typecast into array
        test_data = np.array([Target_Days, Actual_Days, Remaining_Days, Actual_Work, Remaining_Work]).reshape(1,-1)

        
        scale_data = scaler.transform(test_data)

        #Load the model
         

        probability =KNN.predict_proba(scale_data)[0][1]



        print(data)

        if probability >=0.70:
            return render_template('index.html', Data=f" Created Date: {data[0]}, Target Date: {data[1]},\
                        Total Days: {data[4]}, Updated Date : {data[2]}, Actual Days: {data[5]}, Actual Work: {int(data[3])/100},\
                        Remaining Days: {data[6]}, Remaining Work: {data[7]} ", good_progress=f"The probability of doing the \
                        task by the deadline is {round(probability,2)}") # Confidence level: {round(probability[1]*100,1)}%")
        
        if probability <0.70:
             return render_template('index.html', Data=f" Created Date: {data[0]}, Target Date: {data[1]},\
                        Total Days: {data[4]}, Updated Date : {data[2]}, Actual Days: {data[5]}, Actual Work: {int(data[3])/100},\
                        Remaining Days: {data[6]}, Remaining Work: {data[7]} ", bad_progress=f"The probability of doing the \
                        task by the deadline is {round(probability,2)}") # Confidence level: {round(probability[1]*100,1)}%")
        

        
@application.route('/jsondata',methods=['POST', 'GET'])
def jsondata():
    inputs = {"created at" : data[0], "target date": data[1],\
                        "total_days": data[4], "updated date" : data[2], "actual_days": data[5],\
                            "actual_work" : int(data[3])/100,\
                        "remaining_days": data[6], "remaining_work": data[7],"work_probability":round(probability,2)}
                

    return inputs

    


    
        

        
                
if __name__=="__main__":
    application.run(debug=True)
# if __name__=="__main__":
#     app.run(host='0.0.0.0', port=8080)
