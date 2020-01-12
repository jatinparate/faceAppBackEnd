from django.urls import path
from .views import LoginView, UploadView, RecognizeView, MakePresense

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('upload/', UploadView.as_view(), name='uploader'),
    path('recognize/', RecognizeView.as_view(), name='recognizer'),
    path('make_attendance/', MakePresense.as_view(), name='attendanceMaker'),
]
