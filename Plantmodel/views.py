from django.shortcuts import render
from rest_framework import generics
from rest_framework.reverse import reverse
from rest_framework.response import Response
from .models import *
from .serial import *
from django.http import JsonResponse
from rest_framework.decorators import api_view

import joblib , os
import pandas as pd
path_ = os.getcwd()
model = joblib.load(os.path.join(path_ ,"Plantmodel","model_new1.4.2.pkl"))

data = pd.DataFrame({"Sunlight (hours/day)":8.7,
                     "Wind (m/s)":2.3,
                     "pH":6.4,
                     "Soil Type":"Clay",
                     "Temperature (°C)":10.45,
                     "Water (mm/month)":97.32,
                     "Carbon Dioxide (ppm)":350,
                     "Minerals (%)":1.113,} , index = [1])
#print(data)
pred = model.predict(data)

@api_view(["GET"])
def getInput(req):
    """
    This function-based view handles a GET request to modify the last
    entry in the MLModelInput database and then returns all entries.
    
    The reason for this getInput method is to alter the database value 
    to make a prediction and update the database before returning a response 
    to the frontend.
    """
    m = MLModelInput.objects.all()
    if m.exists():  # Check if queryset is not empty
        last_entry = m.last()  # Get the last entry
        last_entry.result = pred  # Modify the result field
        last_entry.save()  # Save the changes to the database
        
    serial = MLModelInputSerial(m, many=True)  # Serialize the data
    return Response(serial.data)  # Return serialized data in the response


class Inputdata(generics.ListCreateAPIView):
    queryset = MLModelInput.objects.all()
    serializer_class = MLModelInputSerial
    name = "input_data"





class APIRoot(generics.GenericAPIView):
     name = "api_root"

     def get(self , req , *args , **kwargs):
          return Response ({
               Inputdata.name : reverse("Plantmodel:"+ Inputdata.name , request=req),
                  })