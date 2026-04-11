from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    dob = models.DateField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

class RandomizerResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='randomizer_results')
    words = models.JSONField()
    created_on = models.DateTimeField(auto_now_add=True)
    
    # Order randomizer results by creation date, newest first
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"Randomizer result for {self.user.username} at {self.created_on}"
    
# Status choices for Story model
STATUS = (
    (0, "Draft"),
    (1, "Published")
)

class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    randomizer = models.OneToOneField(RandomizerResult, on_delete=models.CASCADE, related_name='story')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    genre = models.ForeignKey('Genre', on_delete=models.SET_NULL, null=True, blank=True, related_name='stories')
    
    # Order stories by creation date, newest first
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"Story '{self.title}' by {self.user.username}"
    
    
class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='comments')
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=255)
    comment_text = models.TextField()
    rating = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    # Order comments by creation date, newest first
    class Meta:
        ordering = ['created_on']

    # Adding the author name display method to handle both registered and deleted users
    def display_author(self):
        return self.user.username if self.user else self.author_name

    def __str__(self):
        return f"Comment by {self.display_author()} on '{self.story.title}'"