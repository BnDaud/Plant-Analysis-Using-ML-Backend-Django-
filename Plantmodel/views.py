from django.shortcuts import render
from rest_framework import generics
from rest_framework.reverse import reverse
from rest_framework.response import Response
from .models import *
from .serial import *
from django.http import JsonResponse
from rest_framework.decorators import api_view
import numpy as np
import joblib , os
import pandas as pd
path_ = os.getcwd()
model = joblib.load(os.path.join(path_ ,"Plantmodel","model_new1.4.2.pkl"))
import pandas as pd
import numpy as np

# Assuming these are the columns used during training
columns = [
    "Sunlight (hours/day)", "Wind (m/s)", "pH", "Temperature (°C)", "Water (mm/month)",
    "Carbon Dioxide (ppm)", "Minerals (%)", "Soil Type_Clay", "Soil Type_Loamy", "Soil Type_Sandy"
]

def result(model, last_entry):
    # Prepare the input data as a DataFrame
    input_df = pd.DataFrame({
        "Sunlight (hours/day)": last_entry.sunlight,
        "Wind (m/s)": last_entry.windcurrent,
        "pH": last_entry.phvalue,
        "Soil Type":last_entry.soiltype,
        "Temperature (°C)": last_entry.temperature,
        "Water (mm/month)": last_entry.rainfall,
        "Carbon Dioxide (ppm)": last_entry.humidity,
        "Minerals (%)": last_entry.minerals
    } , index = [0])

    # One-hot encode the input data
    input_encoded = pd.get_dummies(input_df)

    # Ensure the input data has the same columns as the training data
    for col in columns:
        if col not in input_encoded.columns:
            input_encoded[col] = 0

    # Reorder the columns to match the training data
    input_encoded = input_encoded[columns]

    # Make predictions
    pred = model.predict(input_encoded)
    probs = model.predict_proba(input_encoded)

    # Get the class labels
    class_labels = model.classes_

    # Find the top 5 predictions
    top_5_indices = np.argsort(probs[0])[-5:][::-1]
    top_5_plants = class_labels[top_5_indices]
    top_5_predictions = top_5_plants.tolist()

    #print(top_5_predictions)
    str_ = ""
    for i in range(len(top_5_predictions)):
        str_+=top_5_predictions[i]
        str_+=","
    return str_



@api_view(["GET"])
def getInput(req):
    """
    This function-based view handles a GET request to modify the last
    entry in the MLModelInput database and then returns all entries.
    
    The reason for this getInput method is to alter the database value 
    to make a prediction and update the database before returning a response 
    to the frontend.
    """
    dico_crop = {0:"Maize",1:"Wheat",2:"Rice",3:"Sorghum",}
    m = MLModelInput.objects.all()
    if m.exists():  # Check if queryset is not empty
        last_entry = m.last() 
        pred = ... # Get the last entry
        last_entry.result = result(model , last_entry) # Modify the result field
        #print(pred)
        last_entry.save()  # Save the changes to the database
        
    serial = MLModelInputSerial(m, many=True)  # Serialize the data
    return Response(serial.data)  # Return serialized data in the response


class Inputdata(generics.ListAPIView):
    queryset = MLModelInput.objects.all()
    serializer_class = MLModelInputSerial
    name = "input_data"

class Updatedata(generics.RetrieveUpdateAPIView):
    queryset = MLModelInput.objects.all()
    serializer_class = MLModelInputSerial
    name = "input_data"

class APIRoot(generics.GenericAPIView):
     name = "api_root"

     def get(self , req , *args , **kwargs):
          return Response ({
               Inputdata.name : reverse("Plantmodel:"+ Inputdata.name , request=req),
                  })