from django.shortcuts import render
from django.views.generic import TemplateView

# TODO: Подготовить все представления для всех страниц

def response(request):
    return render(request, template_name='./start.html')