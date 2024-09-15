from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.getAll, name='gamer_profile'),
]