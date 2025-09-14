from django.db import models
from django.utils import timezone

# Create your models here.

class ChatSession(models.Model):
    """Session de chat avec un modèle Ollama"""
    pseudo = models.CharField(max_length=15, help_text="Pseudo de l'utilisateur")
    model = models.CharField(max_length=100, help_text="Modèle Ollama utilisé")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, help_text="Session active ou terminée")
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Session {self.pseudo} avec {self.model} ({self.created_at.strftime('%d/%m/%Y %H:%M')})"
    
    def get_message_count(self):
        """Retourne le nombre de messages dans cette session"""
        return self.messages.count()
    
    def get_last_message(self):
        """Retourne le dernier message de la session"""
        return self.messages.order_by('-timestamp').first()

class ChatMessage(models.Model):
    """Message dans une session de chat"""
    SENDER_CHOICES = [
        ('user', 'Utilisateur'),
        ('model', 'Modèle Ollama'),
    ]
    
    session = models.ForeignKey(ChatSession, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField(help_text="Contenu du message")
    is_user = models.BooleanField(default=True, help_text="True si c'est l'utilisateur, False si c'est le modèle")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        sender = "Utilisateur" if self.is_user else "Modèle"
        return f"{sender}: {self.content[:50]}... ({self.timestamp.strftime('%H:%M')})"
    
    @property
    def sender_display(self):
        """Retourne l'affichage du sender"""
        return "Utilisateur" if self.is_user else "Modèle"

