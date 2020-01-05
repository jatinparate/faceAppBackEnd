from django.urls import path
from .views import LoginView, RecognizeView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('recognize/', RecognizeView.as_view(), name='uploader')
]
