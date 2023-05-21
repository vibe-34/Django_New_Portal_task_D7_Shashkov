from django.shortcuts import render


def index(request):
    return render(request, 'new_portal/index.html')


def about(request):
    return render(request, 'new_portal/about.html')

