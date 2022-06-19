from django.conf.urls import url
from django.urls import path
from GetPhotosApi import views

# TEMPLATE TAGGING
app_name = 'GetPhotosApi'

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('gallery/', views.gallery, name='gallery'),
    path('addPhotoFace/', views.addPhotoFace, name='addPhotoFace'),
    path('fetchFromExternalApi/', views.fetchFromExternalApi, name='fetchFromExternalApi'),
    path('fetchFromLocalStorage/', views.fetchFromLocalStorage, name='fetchFromLocalStorage'),
    
    path('photo/<str:pk>/', views.viewPhoto, name='photo'),
]