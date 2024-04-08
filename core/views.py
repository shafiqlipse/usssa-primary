from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages


# Create your views here.
def home(request):
    context = {}
    return render(request, "core/home.html", context)


def district(request):
    context = {}
    return render(request, "", context)


def Officer(request):

    if request.method == "POST":
        form = OfficerForm(request.POST, request.FILES)

        if form.is_valid():
            # admin_user = User.objects.get_or_create(username="admin")
            # Assign the currently logged-in user
            form.save()
            messages.success(request, "Account completed successfully!")
            return redirect("confirmation")

        else:
            # Add form-specific error messages for individual fields
            messages.error(request, "Form is not valid. Please check your input.")
            print(f"Form errors: {form.errors}")

    else:
        form = OfficerForm()

    context = {"form": form}
    return render(request, "school/newofficial.html", context)
