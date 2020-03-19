from django.urls import path
from .views import LoginView, UploadView, RecognizeView, MakePresense, GetAllStudents, GetAverageAttendance, CreateTimeTable, SetSubjectCodes, GetSubjectNames, SendEmail

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('upload/', UploadView.as_view(), name='uploader'),
    path('recognize/', RecognizeView.as_view(), name='recognizer'),
    path('make_attendance/', MakePresense.as_view(), name='attendanceMaker'),
    path('get_average_attendance/', GetAverageAttendance.as_view(), name='averageAttendenceSender'),
    path('createTimeTable/', CreateTimeTable.as_view(), name='timeTableSetter'),
    path('createSubjectCodes/', SetSubjectCodes.as_view(), name='subjectCodesSetter'),
    path('getSubjectNames/', GetSubjectNames.as_view(), name='subjectNamesGetter'),
    path('sendEmail/', SendEmail.as_view(), name='emailSender'),
    path('getStudentsList/', GetAllStudents.as_view(), name='studentsGetter'),
]
