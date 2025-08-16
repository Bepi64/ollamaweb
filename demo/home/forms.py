from django import forms
from django.forms import ModelForm
from .models import ChatSession, ChatMessage

from django.utils import timezone

def create_chat_session(pseudo, model):
    """Fonction utilitaire pour créer une nouvelle session de chat"""
    try:
        # Créer la session
        session = ChatSession.objects.create(
            pseudo=pseudo,
            model=model,
            is_active=True
        )
        return session
    except Exception as e:
        print(f"Erreur lors de la création de la session: {e}")
        return None

def add_message_to_session(session, content, is_user=True):
    """Fonction utilitaire pour ajouter un message à une session"""
    try:
        message = ChatMessage.objects.create(
            session=session,
            content=content,
            is_user=is_user,
            timestamp=timezone.now()
        )
        return message
    except Exception as e:
        print(f"Erreur lors de l'ajout du message: {e}")
        return None
    
