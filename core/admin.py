from django.contrib import admin
from .models import Profile, RandomizerResult, Story, Comment, Genre

# Register your models here.
admin.site.register(Profile)
admin.site.register(RandomizerResult)
admin.site.register(Story)
admin.site.register(Comment)
admin.site.register(Genre)

