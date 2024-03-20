from django.urls import path
from rest_framework import routers

from . import views

router = routers.SimpleRouter()

urlpatterns = [
    path('', views.CompositionView.as_view()),
    path('type/', views.TypesView.as_view())
]