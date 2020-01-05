from django.urls import path
from .views import LoginView, UploadView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('upload/', UploadView.as_view(), name='uploader')
]
