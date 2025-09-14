from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
import re
from ollama import Client

def home(request):
   return render(request, 'index.html')

def model(request):
    try:
        available_models = [hey.model for m in Client(host='http://ollama:11434').list() for hey in m[1]]
        if not available_models:
            print("Available model is an empty list")
    except:
        print("No ollama server found")
        available_models = []

    return render(request, 'model.html', {'models': available_models})
   
@csrf_protect
@require_http_methods(["POST"])
def chat(request):
    pseudo = request.POST.get('pseudo', '').strip()
    if not pseudo:
        return HttpResponse("Le pseudo est obligatoire.", status=400)
    
    if not re.match(r'^[a-zA-Z0-9_:]+$', pseudo):
        return HttpResponse("Le pseudo contient des caractères non autorisés.", status=400)
    
    if len(pseudo) > 15:
        return HttpResponse("Le pseudo est trop long (max 15 caractères).", status=400)
    
    model = request.POST.get('model', '').strip()
    if not model:
        return HttpResponse("Le modèle est obligatoire.", status=400)
    
    if not re.match(r'^[a-zA-Z0-9._:-]+$', model):
        return HttpResponse("Le nom du modèle contient des caractères non autorisés.", status=400)
    
    try:
        available_models = [hey.model for m in Client(host='http://ollama:11434').list() for hey in m[1]]
        if model not in available_models:
            return HttpResponse("Modèle non autorisé.", status=400)
    except Exception as e:
        return HttpResponse("Erreur lors de la vérification du modèle.", status=500)
    
    colon_position = model.find(':')
    if colon_position != -1:  # Si ':' est trouvé
        model = model[:colon_position]
   
    welcome_message = f"Bonjour {pseudo} ! Je suis prêt à discuter avec vous. Que souhaitez-vous me dire ?"
    
    return render(request, 'chat.html', {
        'pseudo': pseudo, 
        'model': model,
    })
