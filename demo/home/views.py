from django.shortcuts import render, HttpResponse
from ollama import list

# Create your views here.
def home(request):
    return render(request, 'index.html')

def model(request):
    list_of_models = ([hey.model for m in list() for hey in m[1]])
    return render(request, 'model.html', {'models': list_of_models})