from django.shortcuts import render, HttpResponse
from ollama import list
import multiprocessing as mp
import subprocess

processs = []

def load_ollama():
    try:
        print("Loading Ollama...")
        subprocess.run(['ollama', 'serve'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error loading Ollama: {e}")

def end_ollama(p):
    if p.is_alive():
        print("Stopping Ollama...")
        p.terminate()
    else:
        print("Ollama process is not running.")


# Create your views here.
def home(request):
    p = mp.Process(target=load_ollama)
    p.start()
    processs.append(p)
    return render(request, 'index.html')

def model(request):
    list_of_models = ([hey.model for m in list() for hey in m[1]])
    return render(request, 'model.html', {'models': list_of_models})
