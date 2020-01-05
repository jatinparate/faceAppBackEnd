from django.urls import path
from .views import LoginView, UploadView, RecognizeView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('upload/', UploadView.as_view(), name='uploader'),
    path('recognize/', RecognizeView.as_view(), name='recognizer'),
]
