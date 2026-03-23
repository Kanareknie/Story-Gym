from django.urls import path
from . import views
from .views import CustomLoginView, CustomLogoutView, register_view

urlpatterns = [
    path('', views.home, name='home'), 
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
    path('randomizer/', views.randomizer, name='randomizer'),
]