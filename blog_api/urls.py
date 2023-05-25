from django.urls import re_path
from . import views

urlpatterns = [
    re_path('start/', views.response, name='start' ),
]