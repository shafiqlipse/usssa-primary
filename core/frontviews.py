from django.shortcuts import render
from school.models import School



# Create your views here.

def home(request):
    context = {}
    return render(request, "core/home.html", context)


def contact(request):

    context = {}
    return render(request, "core/contact.html", context)


def about(request):

    context = {}
    return render(request, "core/about.html", context)


def schooles(request):
    schools = School.objects.all()
    context = {"schools": schools}
    return render(request, "core/schools.html", context)


def faq(request):

    context = {}
    return render(request, "core/faq.html", context)


