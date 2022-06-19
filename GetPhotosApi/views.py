from django.shortcuts import render
from django.http import HttpResponse
from GetPhotosApi.models import *
from django.core import serializers
from GetPhotosApi.serializers import *

from django.http import JsonResponse
import json

import requests, logging

import shutil
import base64

# PARAMETERS -------------------------------------------------------------------------------------------
CALL_EXTERNAL_API = True                  # Set FALSE when want to load local JSON for testing purposes

# Create your views here.
def index(request):
    dcontext = {
        'access_records': [],
        'text':'hello world',
        'number':100
    }
    return render(request, 'GetPhotosApi/index.html', context = dcontext)

# Helper functions
def addParamsToURL(iURL, iForm_params):
    result = iURL
    for par in iForm_params:
        if iForm_params[par]:
            if par in ['gender', 'age', 'ethnicity', 'eye_color', 'hair_color', 'hair_length', 'emotion']:
                par_val = iForm_params[par]
                result = result+"&"+par+"="+par_val
    return result

def get_image(url):
    img = requests.get(url, stream=True)
    with open('temp.jpg', 'wb') as f:
        shutil.copyfileobj(img.raw, f)
    del img
    return 'temp.jpg'

def img_base64(file_name):
    with open(file_name , "rb") as image_file :
        data = base64.b64encode(image_file.read())
    return data.decode('utf-8')

def getValidKeyFromDB(iDBObject):
    for itemKey in iDBObject:
        serializedKeyItem = serializers.serialize('json', [ itemKey, ])
        JSONKey = json.loads(serializedKeyItem)
        key_value = JSONKey[0]['fields']['key']
        if len(key_value)>0:
            return key_value
        else:
            return 'None'

def filterList(iObjectList, iParams):
    result = iObjectList
    for par in iParams:
        if iParams[par]:
            par_name = str(par)
            par_val = str(iParams[par])
  
            if par in ['gender', 'age', 'ethnicity', 'eye_color', 'hair_color', 'hair_length', 'emotion']:
                # c = 0
                aux=[]
                for itemObject in result:
                    if par_name=='emotion' and str(itemObject.category_emotion)==par_val:
                        aux.append(itemObject)
                        print('Found a match')
                    if (par_name=='gender'or par_name.casefold()=='sex') and str(itemObject.category_gender)==par_val:
                        aux.append(itemObject) 
                        print('Found a match')
                    if par_name=='age' and str(itemObject.category_age)==par_val:
                        aux.append(itemObject) 
                        print('Found a match')
                    if par_name=='ethnicity' and str(itemObject.category_ethnicity)==par_val:
                        aux.append(itemObject) 
                        print('Found a match')
                    if par_name=='eye_color' and str(itemObject.category_eye_color)==par_val:
                        aux.append(itemObject) 
                        print('Found a match')
                    if par_name=='hair_color' and str(itemObject.category_hair_color)==par_val:
                        aux.append(itemObject) 
                        print('Found a match')
                    if par_name=='hair_length' and str(itemObject.category_hair_length)==par_val:
                        aux.append(itemObject) 
                        print('Found a match')
                    
                    # c+=1
                result = aux
    return result

# Other functions
def fetchFromExternalApi(request):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":
        # get the form data
        PostData = request.POST
        response = {}
        failed_api_call = False
        if CALL_EXTERNAL_API:
            # Get loggin key
            myKey = getValidKeyFromDB(GeneratedFacesAPIKey.objects.all())
            print('API Key=', myKey)
            if myKey != 'None':
                # Make an external api request ( use auth if authentication is required for the external API)
                print('calling external api..')
                API_URL="https://api.generated.photos/api/v1/faces?api_key="+myKey
                API_URL = addParamsToURL(API_URL, PostData)
                print('URL=', API_URL)

                try:
                    print('Finish calling to external api')
                    r = requests.get(API_URL)
                    r_status = r.status_code
                    # If it is a success
                    if r_status == 200:
                        response['status'] = 200
                        response['message'] = 'success'
                        data = r.json()
                        response['data'] = data
                    else:
                        response['status'] = r.status_code
                        response['message'] = 'error'
                        response['data'] = {}
                    return JsonResponse({"photos_group": response}, status=200)
                except:
                    failed_api_call = True
                    logging.WARNING(f"Fetch models from {API_URL} failed")
            else:
                failed_api_call = True
                print('Could not find a valid Key to call the external Api')

    else:
        # some form errors occured.
        return JsonResponse({"error": []}, status=400)

def gallery(request):
    photos = PhotoFace.objects.all()
    context = {
        'photos':photos}
    return render(request, 'GetPhotosApi/gallery.html', context = context)

def fetchFromLocalStorage(request):
    print('BackEnd fetchFromLocalStorage fnc...')
    if request.is_ajax and request.method == "POST":
        # get the form data
        PostData = request.POST
        response = {}
        photos = PhotoFace.objects.all()

        # filter photos by from parameters
        filtered = filterList(photos, PostData)
        serializedPhotos = PhotoSerializer2(filtered, many=True)
        serializedPhotosJSON = json.dumps(serializedPhotos.data)

        response['status'] = 200
        response['message'] = 'success'
        response['data'] = serializedPhotosJSON
        return JsonResponse({"photos_group": response}, status=200)
    else:
        # some form errors occured.
        return JsonResponse({"error": []}, status=400)

def addPhotoFace(request):
    if request.is_ajax and request.method == "POST":
        func_response = {}

        # get the form data
        PostData = request.POST

        d_URL = PostData['url']
        d_Meta = PostData['meta']
        d_Meta_JSON = json.loads(PostData['meta'])
        if ('emotion' in d_Meta_JSON) and (d_Meta_JSON['emotion'][0] != 'none'):
            category_emotion, created = CategoryEmotion.objects.get_or_create(name=d_Meta_JSON['emotion'][0])
        else:
            category_emotion = None

        if ('gender' in d_Meta_JSON) and (d_Meta_JSON['gender'][0] != 'none'):
            category_gender, created = CategoryGender.objects.get_or_create(name=d_Meta_JSON['gender'][0])
        else:
            category_gender = None

        if d_Meta_JSON['age'] and d_Meta_JSON['age'][0] != 'none':
            category_age, created = CategoryAge.objects.get_or_create(name=d_Meta_JSON['age'][0])
        else:
            category_age = None

        if d_Meta_JSON['ethnicity'] and d_Meta_JSON['ethnicity'][0] != 'none':
            category_ethnicity, created = CategoryEthnicity.objects.get_or_create(name=d_Meta_JSON['ethnicity'][0])
        else:
            category_ethnicity = None

        if d_Meta_JSON['eye_color'] and d_Meta_JSON['eye_color'][0] != 'none':
            category_eye_color, created = CategoryEyeColor.objects.get_or_create(name=d_Meta_JSON['eye_color'][0])
        else:
            category_eye_color = None

        if d_Meta_JSON['hair_color'] and d_Meta_JSON['hair_color'][0] != 'none':
            category_hair_color, created = CategoryHairColor.objects.get_or_create(name=d_Meta_JSON['hair_color'][0])
        else:
            category_hair_color = None

        if d_Meta_JSON['hair_length'] and d_Meta_JSON['hair_length'][0] != 'none':
            category_hair_length, created = CategoryHairLength.objects.get_or_create(name=d_Meta_JSON['hair_length'][0])
        else:
            category_hair_length = None

        imagen = img_base64(get_image(d_URL))

        photoface = PhotoFace.objects.create(
            category_emotion      = category_emotion,
            category_gender       = category_gender,
            category_age          = category_age,
            category_ethnicity    = category_ethnicity,
            category_eye_color    = category_eye_color,
            category_hair_color   = category_hair_color,
            category_hair_length  = category_hair_length,
            description = "description",
            image = imagen
        )

        func_response['status'] = 200
        func_response['message'] = 'success'
        func_response['data']={}

        return JsonResponse({"response": func_response}, status=200)

def viewPhoto(request, pk):
    photo = PhotoFace.objects.get(id=pk)
    context={
         'photo':photo
    }
    return render(request, 'GetPhotosApi/photo.html', context = context)

