from django.urls import path, re_path
from .views import *

app_name = "Plantmodel"

urlpatterns = [
    path("getInputs/" ,view=getInput , name = "getInputs" ),
    path (Inputdata.name+"/" , view=Inputdata.as_view(), name=Inputdata.name),
    path (Updatedata.name+"/<int:pk>" , view=Updatedata.as_view(), name=Updatedata.name),
    path("" , view=APIRoot.as_view(), name=APIRoot.name)
    
]