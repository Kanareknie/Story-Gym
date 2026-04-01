from django.urls import path
from . import views
from .views import CustomLoginView, CustomLogoutView, register_view, randomizer_view, write_now_view, my_story_view, preview_story_view, repo_view, account_view, edit_story_view, delete_story_view

urlpatterns = [
    path('', views.home, name='home'), 
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
    path('randomizer/', views.randomizer_view, name='randomizer'),
    path('write_now/', views.write_now_view, name='write_now'),
    path('my_story/', views.my_story_view, name='my_story'),
    path('preview_story/<int:story_id>/', views.preview_story_view, name='preview_story'),
    path('repo/', views.repo_view, name='repo_story'),
    path('account/', views.account_view, name='account'),
    path('story/<int:story_id>/edit/', views.edit_story_view, name='edit_story'),
    path('story/<int:story_id>/delete/', views.delete_story_view, name='delete_story'),

    
]