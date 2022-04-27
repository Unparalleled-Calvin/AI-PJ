from django.shortcuts import render

# Create your views here.
def servey(request):
    return render(request, "servey.html")