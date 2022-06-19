from django.db import models

# Create your models here.
class CategoryEmotion(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    def __str__(self):
        return self.name

class CategoryGender(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    def __str__(self):
        return self.name

class CategoryAge(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    def __str__(self):
        return self.name

class CategoryEthnicity(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    def __str__(self):
        return self.name

class CategoryEyeColor(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    def __str__(self):
        return self.name

class CategoryHairColor(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    def __str__(self):
        return self.name

class CategoryHairLength(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    def __str__(self):
        return self.name

class PhotoFace(models.Model):
    category_emotion      = models.ForeignKey(CategoryEmotion, null=True, blank=True, on_delete=models.SET_NULL)
    category_gender       = models.ForeignKey(CategoryGender, null=True, blank=True, on_delete=models.SET_NULL)
    category_age          = models.ForeignKey(CategoryAge, null=True, blank=True, on_delete=models.SET_NULL)
    category_ethnicity    = models.ForeignKey(CategoryEthnicity, null=True, blank=True, on_delete=models.SET_NULL)
    category_eye_color    = models.ForeignKey(CategoryEyeColor, null=True, blank=True, on_delete=models.SET_NULL)
    category_hair_color   = models.ForeignKey(CategoryHairColor, null=True, blank=True, on_delete=models.SET_NULL)
    category_hair_length  = models.ForeignKey(CategoryHairLength, null=True, blank=True, on_delete=models.SET_NULL)
    
    image = models.ImageField(null=False, blank=False)
    description = models.TextField()

    def __str__(self):
        result=""
        if len(self.description)>0:
            return self.description
        else:
            return self.category_gender+" "+self.category_emotion+" "+self.category_age+" "+self.category_ethnicity+" "+self.category_eye_color+" "+self.category_hair_color+" "+self.category_hair_length

class GeneratedFacesAPIKey(models.Model):
    description = models.TextField()
    key = models.TextField()

    def __str__(self):
        return self.description