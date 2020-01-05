from django.http import HttpResponse, HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

import os

import firebase_admin
from firebase_admin import credentials, db

from faceAppBackend.forms import PhotoForm

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

        return JsonResponse({'is_logged_in' : False})


@method_decorator(csrf_exempt, name='dispatch')
class UploadView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse("Recognize View")

    def post(self, request: HttpRequest, *args, **kwargs):
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)
