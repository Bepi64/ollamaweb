from django.urls import path
from . import views

urlpatterns = [
        path("", views.home, name="home"),
        path("model.html", views.model, name="model"),
        path("chat/", views.chat, name="chat"),
]
