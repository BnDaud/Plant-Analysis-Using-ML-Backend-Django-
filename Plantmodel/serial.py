from rest_framework.serializers import ModelSerializer
from .models import *


class MLModelInputSerial(ModelSerializer):
    
    class Meta:
        model = MLModelInput
        fields = "__all__"

