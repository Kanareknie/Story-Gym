from django.urls import path
from . import views
from .views import CustomLoginView, CustomLogoutView, register_view, randomizer_view, my_story_view

urlpatterns = [
    path('', views.home, name='home'), 
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
    path('randomizer/', views.randomizer_view, name='randomizer'),
    path('my_story/', views.my_story_view, name='my_story'),
]