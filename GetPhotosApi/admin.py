from django.contrib import admin
from GetPhotosApi.models import *

# Register your models here.
admin.site.register(CategoryEmotion)
admin.site.register(CategoryGender)
admin.site.register(CategoryAge)
admin.site.register(CategoryEthnicity)
admin.site.register(CategoryEyeColor)
admin.site.register(CategoryHairColor)
admin.site.register(CategoryHairLength)
admin.site.register(PhotoFace)
admin.site.register(GeneratedFacesAPIKey)
