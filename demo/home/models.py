from django.db import models

# Create your models here.
class HumanMessage(models.Model):
    author = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    ai_receiver = models.CharField(max_length=100)

class BotMessage(models.Model):
    ai_sender = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)