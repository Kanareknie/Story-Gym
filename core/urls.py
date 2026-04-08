from django.urls import path
from . import views
from .views import CustomLoginView, CustomLogoutView, register_view, randomizer_view, write_now_view, my_story_view, preview_story_view, repo_view, account_view, edit_story_view, delete_story_view, edit_comment_view, delete_comment_view, article_whats_new_view
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
    path('randomizer/', views.randomizer_view, name='randomizer'),
    path('write_now/', views.write_now_view, name='write_now'),
    path('my_story/', views.my_story_view, name='my_story'),
    path('preview_story/<int:story_id>/',
         views.preview_story_view, name='preview_story'),
    path('repo/', views.repo_view, name='repo_story'),
    path('account/', views.account_view, name='account'),
    path('story/<int:story_id>/edit/', views.edit_story_view, name='edit_story'),
    path('story/<int:story_id>/delete/',
         views.delete_story_view, name='delete_story'),
    path('comment/<int:comment_id>/edit/',
         views.edit_comment_view, name='edit_comment'),
    path('comment/<int:comment_id>/delete/',
         views.delete_comment_view, name='delete_comment'),
    path('articles/article_whats_new/', views.article_whats_new_view, name='article_whats_new'),

     # Password reset views
     # https://docs.djangoproject.com/en/4.2/topics/auth/default/#using-the-views
     # https://docs.djangoproject.com/en/4.2/_modules/django/contrib/auth/views/?utm_source=chatgpt.com # for more info on the password reset views and how to customize them
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.html',
            subject_template_name='registration/password_reset_subject.txt',
        ),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html',
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html',
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html',
        ),
        name='password_reset_complete'
    ),

]


