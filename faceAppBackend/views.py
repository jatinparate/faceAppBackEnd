import os
import shutil
from datetime import date, datetime, timedelta
import smtplib, ssl

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
        faculties = db.reference('/Faculties/').get() or {}
        for faculty in faculties:
            if faculty['email'] == posted_details[0] and faculty['password'] == posted_details[1]:
                return JsonResponse({'is_logged_in': True, 'email': faculty['email'], 'name': faculty['name']})

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
        sem = request.data['sem']
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
        students = db.reference('/students/' + branch + '/' + class_str + '/').get() or {}
        list_of_students = []
        for enrollment_no in students:
            student = db.reference('/students/' + branch + '/' + class_str + '/' + enrollment_no).get() or {}
            is_present = False
            if student['sem'] == sem:
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
            request.data['sem'] +
            '/' +
            today.strftime("%d%m%Y") +
            '/' +
            request.data['lacture_no'] +
            '/'
        )
        students = students_ref.get() or {}
        for student in request.data['students']:
            students[student['enrollment_no']] = student['is_present']
        print(students)
        students_ref.set(students)
        return JsonResponse({'is_successful': True})


@method_decorator(csrf_exempt, name='dispatch')
class CreateTimeTable(APIView):
    def post(self, request):
        timetable_ref = db.reference('/timetable/')
        timetable = {
            'CE': {
                'sem-1': {
                    1: {
                        1: 3110005,
                        2: 3110002,
                        3: 3110014,
                        4: 3110013,
                        5: 3110014,
                    },
                    2: {
                        1: 3110011,
                        2: 3110013,
                        3: 3110005,
                        4: 3110002,
                        5: 3110014,
                    },
                    3: {
                        1: 3110005,
                        2: 3110002,
                        3: 3110014,
                        4: 3110013,
                        5: 3110014,
                    },
                    4: {
                        1: 3110011,
                        2: 3110013,
                        3: 3110005,
                        4: 3110002,
                        5: 3110014,
                    },
                    5: {
                        1: 3110005,
                        2: 3110002,
                        3: 3110014,
                        4: 3110013,
                        5: 3110014,
                    },
                },
                'sem-2': {
                    1: {
                        1: 3110007,
                        2: 3110013,
                        3: 3110015,
                        4: 3110013,
                        5: 3110018,
                    },
                    2: {
                        1: 3110003,
                        2: 3110018,
                        3: 3110016,
                        4: 3110013,
                        5: 3110003,
                    },
                    3: {
                        1: 3110007,
                        2: 3110015,
                        3: 3110003,
                        4: 3110015,
                        5: 3110018,
                    },
                    4: {
                        1: 3110007,
                        2: 3110013,
                        3: 3110015,
                        4: 3110013,
                        5: 3110018,
                    },
                    5: {
                        1: 3110003,
                        2: 3110018,
                        3: 3110016,
                        4: 3110013,
                        5: 3110003,
                    },
                },
                'sem-3': {
                    1: {
                        1: 3130004,
                        2: 3130007,
                        3: 3130704,
                        4: 3130703,
                        5: 3130006,
                    },
                    2: {
                        1: 3130704,
                        2: 3130703,
                        3: 3130702,
                        4: 3130004,
                        5: 3130006,
                    },
                    3: {
                        1: 3130004,
                        2: 3130007,
                        3: 3130704,
                        4: 3130703,
                        5: 3130006,
                    },
                    4: {
                        1: 3130704,
                        2: 3130703,
                        3: 3130702,
                        4: 3130004,
                        5: 3130006,
                    },
                    5: {
                        1: 3130703,
                        2: 3130704,
                        3: 3130004,
                        4: 3130006,
                        5: 3130702,
                    },
                },
                'sem-4': {
                    1: {
                        1: 2140002,
                        2: 2140705,
                        3: 2140702,
                        4: 2140706,
                        5: 2140709,
                    },
                    2: {
                        1: 2140707,
                        2: 2140709,
                        3: 2140706,
                        4: 2140002,
                        5: 2140702,
                    },
                    3: {
                        1: 2140002,
                        2: 2140705,
                        3: 2140702,
                        4: 2140706,
                        5: 2140709,
                    },
                    4: {
                        1: 2140707,
                        2: 2140709,
                        3: 2140706,
                        4: 2140002,
                        5: 2140702,
                    },
                    5: {
                        1: 2140702,
                        2: 2140002,
                        3: 2140709,
                        4: 2140706,
                        5: 2140707,
                    },
                },
                'sem-5': {
                    1: {
                        1: 2150001,
                        2: 2150704,
                        3: 2150703,
                        4: 2150707,
                        5: 2150708,
                    },
                    2: {
                        1: 2150002,
                        2: 2150003,
                        3: 2150707,
                        4: 2150003,
                        5: 2150708,
                    },
                    3: {
                        1: 2150001,
                        2: 2150704,
                        3: 2150703,
                        4: 2150707,
                        5: 2150708,
                    },
                    4: {
                        1: 2150002,
                        2: 2150003,
                        3: 2150707,
                        4: 2150003,
                        5: 2150708,
                    },
                    5: {
                        1: 2150001,
                        2: 2150704,
                        3: 2150703,
                        4: 2150707,
                        5: 2150708,
                    },
                },
                'sem-6': {
                    1: {
                        1: 2160001,
                        2: 2160707,
                        3: 2160710,
                        4: 2160704,
                        5: 2160703,
                    },
                    2: {
                        1: 2160703,
                        2: 2160709,
                        3: 2160704,
                        4: 2160701,
                        5: 2160711,
                    },
                    3: {
                        1: 2160001,
                        2: 2160707,
                        3: 2160710,
                        4: 2160704,
                        5: 2160703,
                    },
                    4: {
                        1: 2160703,
                        2: 2160709,
                        3: 2160704,
                        4: 2160701,
                        5: 2160711,
                    },
                    5: {
                        1: 2160001,
                        2: 2160707,
                        3: 2160710,
                        4: 2160704,
                        5: 2160703,
                    },
                },
                'sem-7': {
                    1: {
                        1: 2170001,
                        2: 2170709,
                        3: 2170710,
                        4: 2170713,
                        5: 2170715,
                    },
                    2: {
                        1: 2170712,
                        2: 2170710,
                        3: 2170701,
                        4: 2170001,
                        5: 2170712,
                    },
                    3: {
                        1: 2170001,
                        2: 2170709,
                        3: 2170710,
                        4: 2170713,
                        5: 2170715,
                    },
                    4: {
                        1: 2170712,
                        2: 2170710,
                        3: 2170701,
                        4: 2170001,
                        5: 2170712,
                    },
                    5: {
                        1: 2170001,
                        2: 2170709,
                        3: 2170710,
                        4: 2170713,
                        5: 2170715,
                    },
                },
                'sem-8': {
                    3: {
                        3: 2180714,
                        4: 2180703,
                        5: 2180703
                    },
                    4: {
                        1: 2180703,
                        3: 2180703,
                        4: 2180703,
                    },
                    5: {
                        2: 2180714,
                        3: 2180714,
                        4: 2180714,
                        5: 2180711,
                    }
                }
            }
        }
        timetable_ref.set(timetable)
        return JsonResponse({
            'data': 'data'
        })


@method_decorator(csrf_exempt, name='dispatch')
class SetSubjectCodes(APIView):
    def post(self, request):
        subjectCodes_ref = db.reference('/subjectCodes/')
        subjectCodes = {
            'CE': {
                'sem-1': {
                    3110002: 'English',
                    3110005: 'Basic Electrical Engineering',
                    3110011: 'Physics Group - I',
                    3110012: 'Workshop',
                    3110013: 'Engineering Graphics & Design',
                    3110014: 'Maths-Mathematics-I',
                },
                'sem-2': {
                    3110007: 'Environmental Science',
                    3110003: 'Programming for Problem Solving',
                    3110013: 'Engineering Graphics & Design',
                    3110015: 'Maths-Mathematics-II',
                    3110016: 'Basic Electronics',
                    3110018: 'Physics Group - II',
                },
                'sem-3': {
                    3130004: 'Effective Technical Communication',
                    3130006: 'Probability and Statistics',
                    3130007: 'Indian Constitution',
                    3130008: 'Design Engineering',
                    3130702: 'Data Structures    3',
                    3130703: 'Database Management Systems',
                    3130704: 'Digital Fundamental',
                },
                'sem-4': {
                    2140002: 'Design Engineering',
                    2140702: 'Operating System',
                    2140705: 'Object Oriented Programming With C++',
                    2140706: 'Numerical and Statistical Methods for Computer Engineering',
                    2140707: 'Computer Organization',
                    2140709: 'Computer Networks',
                },
                'sem-5': {
                    2150001: 'Design Engineering - II A',
                    2150002: 'Cyber Security (Inst Elec)',
                    2150003: 'Disaster Management (Inst Elec)',
                    2150703: 'Analysis and Design of Algorithms',
                    2150704: 'Object Oriented Programming using JAVA',
                    2150707: 'Microprocessor and Interfacing',
                    2150708: 'System Programming',
                },
                'sem-6': {
                    2160001: 'Design Engineering - II B',
                    2160701: 'Software Engineering',
                    2160703: 'Computer Graphics (Dept Elec-I)',
                    2160704: 'Theory of Computation',
                    2160707: 'Advanced Java',
                    2160708: 'Web Technology',
                    2160709: 'Embedded and VLSI Design (Dept Elec-I)',
                    2160710: 'Distributed Operating System (Dept Elec-I)',
                    2160711: 'Dot Net Technology (Dept Elec-I)',
                },
                'sem-7': {
                    2170001: 'Project',
                    2170701: 'Complier Design',
                    2170709: 'Information and Network Security',
                    2170710: 'Mobile Computing and Wireless Communication',
                    2170712: 'Image Processing (Dept Elec-II)',
                    2170713: 'Service Oriented Computing (Dept Elec-II)',
                    2170714: 'Distributed DBMS (Dept Elec-II)',
                    2170715: 'Data Mining and Business Intelligence (Dept Elec-II)',
                },
                'sem-8': {
                    2180703: 'Artificial Intelligence',
                    2180706: 'Project (Phase-II)',
                    2180709: 'IOT and Applications (Dept Elec - III)',
                    2180710: 'Big Data Analytics (Dept Elec - III)',
                    2180711: 'Python Programming (Dept Elec - III)',
                    2180712: 'Cloud Infrastructure and Services (Dept Elec - III)',
                    2180713: 'Web Data Management (Dept Elec - III)',
                    2180714: 'iOS Programming (Dept Elec - III)',
                    2180715: 'Android Programming (Dept Elec - III)',
                }
            }
        }
        subjectCodes_ref.set(subjectCodes)
        return JsonResponse({
            'is_created': True
        })


@method_decorator(csrf_exempt, name='dispatch')
class GetSubjectNames(APIView):
    def post(self, request):
        subjectCodes = db.reference(
            '/subjectCodes/' + request.data['branch'] + '/' + request.data['sem'] + '/').get() or {}

        return JsonResponse({
            'subjectCodes': subjectCodes
        })


@method_decorator(csrf_exempt, name='dispatch')
class GetAverageAttendance(APIView):
    def post(self, request):
        attendance = db.reference(
            '/attendance/' + request.data['branch'] + '/' + request.data['class_str'] + '/' + request.data[
                'sem'] + '/').get() or {}

        sem_starting_date = db.reference('/sem-starting-dates/' + request.data['sem']).get() or {}
        cur_date = datetime.now()
        sem_starting_date = datetime.strptime(sem_starting_date['date'], '%d%m%Y').date()
        sem_starting_date = datetime(sem_starting_date.year, sem_starting_date.month, sem_starting_date.day)

        present_lacture_count = 0
        total_lacture_count = 0
        while sem_starting_date <= cur_date:

            try:
                if attendance[cur_date.strftime('%d%m%Y')]:
                    for i in range(1, 6):
                        at = db.reference('/attendance/' + request.data['branch'] +
                                          '/' + request.data['class_str'] + '/' +
                                          request.data['sem'] + '/' + cur_date.strftime('%d%m%Y') + '/' +
                                          str(i) + '/').get() or {}
                        if at[request.data['enrollment']]:
                            present_lacture_count += 1

                        total_lacture_count += 1
            except:
                print('')
            cur_date = cur_date + timedelta(days=-1)
        return JsonResponse({
            'total': total_lacture_count,
            'present': present_lacture_count
        })


@method_decorator(csrf_exempt, name='dispatch')
class SendEmail(APIView):
    def post(self, request):
        enrollment = request.data['enrollment']
        branch = request.data['branch']
        class_str = request.data['class_str']
        total_lactures = request.data['total_lactures']
        present_lactures = request.data['present_lactures']
        student = db.reference('/students/' + branch + '/' + class_str + '/' + enrollment + '/').get() or {}
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login("jatin4228@gmail.com", 'japarate')
            server.sendmail('jatin4228@gmail.com', student['parent_email'],
                            'Your child ' + student['name'] + ' was present in ' + str(present_lactures) + ' out of ' +
                            str(total_lactures) + '. Please pay attension to your child!!'
                            )
            return JsonResponse({'msg': 'sent'})
