
from rest_framework import serializers as rest_serializers
from django.db import models

from GetPhotosApi.models import PhotoFace

class PhotoSerializer2(rest_serializers.Serializer):
    pk                  = rest_serializers.UUIDField()
    category_emotion    = rest_serializers.CharField(max_length = 200)
    category_gender     = rest_serializers.CharField(max_length = 200)
    category_age        = rest_serializers.CharField(max_length = 200)
    category_ethnicity  = rest_serializers.CharField(max_length = 200)
    category_eye_color  = rest_serializers.CharField(max_length = 200)
    category_hair_color = rest_serializers.CharField(max_length = 200)
    category_hair_length= rest_serializers.CharField(max_length = 200)

    image = rest_serializers.CharField()
    description = rest_serializers.CharField(max_length = 200)

    class Meta:
        model = PhotoFace
        fields ='__all__'
