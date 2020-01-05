from django.http import HttpResponse, HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

import os

from .helpers import modify_input_for_multiple_files

import firebase_admin
from firebase_admin import credentials, db
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView

from faceAppBackend.models import Image
from faceAppBackend.serializers import ImageSerializer

cred = credentials.Certificate(os.getcwd() + '/creds.json')
firebase_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://faceapp-db03e.firebaseio.com/'
})
root = db.reference()


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse("GET")

    def post(self, request: HttpRequest, *args, **kwargs):
        posted_details = [value for item, value in request.POST.items()]
        faculties = db.reference('/Faculties/').get()
        for faculty in faculties:
            if faculty['email'] == posted_details[0] and faculty['password'] == posted_details[1]:
                return JsonResponse({'is_logged_in': True})

        return JsonResponse({'is_logged_in': False})


@method_decorator(csrf_exempt, name='dispatch')
class UploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        all_images = Image.objects.all()
        serializer = ImageSerializer(all_images, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        property_id = request.data['property_id']
        branch = request.data['branch']
        class_str = request.data['class_str']
        images = dict((request.data).lists())['image']
        flag = 1
        arr = []
        for image_name in images:
            modified_data = modify_input_for_multiple_files(property_id, branch, class_str, image_name)
            file_serializer = ImageSerializer(data=modified_data)
            if file_serializer.is_valid():
                file_serializer.save()
                arr.append(file_serializer.data)
            else:
                flag = 0
        if flag == 1:
            return JsonResponse({"is_uploaded": True})
        else:
            return JsonResponse({"is_uploaded": False})

@method_decorator(csrf_exempt, name='dispatch')
class RecognizeView(APIView):
    pass
