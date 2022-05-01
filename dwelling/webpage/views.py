from django.shortcuts import render
from urllib.parse import unquote

# Create your views here.
def servey(request):
    if request.method == "POST":
        data = parse_data(unquote(request.body.decode()))
    return render(request, "servey.html")

def parse_data(data_str: str):
    data = {}
    for pair in data_str.split("&"):
        k,v = pair.split("=")
        data[k] = v
    return data