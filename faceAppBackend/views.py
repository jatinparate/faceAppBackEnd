import os
import shutil
from datetime import date

import firebase_admin
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from firebase_admin import credentials, db
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView

from faceAppBackend.models import Image
from faceAppBackend.serializers import ImageSerializer
from .helpers import modify_input_for_multiple_files, image_classifier

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
    def get(self, request):
        output_arr = image_classifier()
        return JsonResponse({'output': output_arr})

    def post(self, request):
        class_str = request.data['class_str']
        branch = request.data['branch']
        output_arr = image_classifier()

        folder = os.path.join(os.getcwd(), 'media', 'images')
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

        # get all students in given class and div from database
        students = db.reference('/students/' + class_str + '/' + branch + '/').get()
        list_of_students = []
        for enrollment_no in students:
            student = db.reference('/students/' + class_str + '/' + branch + '/' + enrollment_no).get()
            is_present = False
            for output_student in output_arr:
                if output_student['predicted_enroll_no'] == enrollment_no:
                    is_present = True
            list_of_students.append({
                'enrollment_no': enrollment_no,
                'name': student['name'],
                'is_present': is_present
            })
        return JsonResponse({
            'class': class_str,
            'branch': branch,
            # 'output': output_arr,
            'students': list_of_students
        })


@method_decorator(csrf_exempt, name='dispatch')
class MakePresense(APIView):
    def post(self, request):
        today = date.today()
        students_ref = db.reference(
            '/attendance/' +
            request.data['class'] +
            '/' +
            request.data['division'] +
            '/' +
            today.strftime("%d%m%Y") +
            '/'
        )
        students = students_ref.get()
        for student in request.data['students']:
            students[student['enrollment_no']] = student['is_present']
        print(students)
        students_ref.set(students)
        return JsonResponse({'is_successful': True})
