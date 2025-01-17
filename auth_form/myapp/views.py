from django.shortcuts import render

def registration_view(request):
    return render(request, 'myapp/registration.html')