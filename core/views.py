from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib import messages
from accounts.decorators import anonymous_required, admin_required, staff_required
from .models import *


# Create your views here.
def home(request):
    context = {}
    return render(request, "core/home.html", context)

