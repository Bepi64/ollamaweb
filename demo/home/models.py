from django.db import models

# Create your models here.

class Session(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    sender = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    receiver = models.CharField(max_length=100)
    session = models.ForeignKey(Session, related_name='messages', on_delete=models.CASCADE)