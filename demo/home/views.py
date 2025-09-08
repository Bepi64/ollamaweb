from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
import re
from ollama import Client

available_models = [hey.model for m in Client(host='http://ollama:11434').list() for hey in m[1]]

# Create your views here.
def home(request):
   return render(request, 'index.html')

def model(request):
    return render(request, 'model.html', {'models': available_models})
   
@csrf_protect
@require_http_methods(["POST"])
def chat(request):
    # Validation et nettoyage du pseudo
    pseudo = request.POST.get('pseudo', '').strip()
    if not pseudo:
        return HttpResponse("Le pseudo est obligatoire.", status=400)
    
    # Validation du pseudo avec re.match (format strict)
    if not re.match(r'^[a-zA-Z0-9_:]+$', pseudo):
        return HttpResponse("Le pseudo contient des caractères non autorisés.", status=400)
    
    # Limiter la taille du pseudo
    if len(pseudo) > 15:
        return HttpResponse("Le pseudo est trop long (max 15 caractères).", status=400)
    
    # Validation et nettoyage du modèle
    model = request.POST.get('model', '').strip()
    if not model:
        return HttpResponse("Le modèle est obligatoire.", status=400)
    
    # Validation du modèle avec re.match (format strict)
    if not re.match(r'^[a-zA-Z0-9._:-]+$', model):
        return HttpResponse("Le nom du modèle contient des caractères non autorisés.", status=400)
    
    # Vérifier que le modèle existe dans la liste des modèles disponibles
    try:
        if model not in available_models:
            return HttpResponse("Modèle non autorisé.", status=400)
    except Exception as e:
        return HttpResponse("Erreur lors de la vérification du modèle.", status=500)
    
    # Traiter le nom du modèle (enlever la version si présente)
    colon_position = model.find(':')
    if colon_position != -1:  # Si ':' est trouvé
        model = model[:colon_position]
   
    # Ajouter le message de bienvenue du modèle
    welcome_message = f"Bonjour {pseudo} ! Je suis prêt à discuter avec vous. Que souhaitez-vous me dire ?"
    
    return render(request, 'chat.html', {
        'pseudo': pseudo, 
        'model': model,
    })
