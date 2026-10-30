from django.shortcuts import render


def home(request):
    return render(request, "djangoapp/home.html")


def about(request):
    return render(request, "djangoapp/about.html")


def contact(request):
    return render(request, "djangoapp/contact.html")
