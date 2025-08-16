from django.apps import AppConfig
import multiprocessing as mp
import subprocess

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


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'