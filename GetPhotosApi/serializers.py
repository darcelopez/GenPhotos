# from django.core import serializers
from rest_framework import serializers as rest_serializers
from django.db import models
# from drf_extra_fields.fields import Base64ImageField

from GetPhotosApi.models import PhotoFace

# class MyImageModel(models.Model):
#       image = models.ImageField(upload_to = 'geo_entity_pic')
#       data = models.CharField()

# class MyImageModelSerializer(rest_serializers.Serializer):
#     image=Base64ImageField() # From DRF Extra Fields
#     class Meta:
#         model=MyImageModel
#         fields= ('data','image')
#     def create(self, validated_data):
#         image=validated_data.pop('image')
#         data=validated_data.pop('data')
#         return MyImageModel.objects.create(data=data,image=image)


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
    # image = MyImageModelSerializer
    description = rest_serializers.CharField(max_length = 200)

    class Meta:
        model = PhotoFace
        fields ='__all__'
