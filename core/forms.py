from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile, Story, Comment, Genre
import re
from datetime import date


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=15, required=True)
    # User table - add email
    email = forms.EmailField(required=True)
    # Profile table - add dob, security question and
    # answer only to reset the password purpuse
    dob = forms.DateField(
        required=True, widget=forms.DateInput(attrs={'type': 'date'}))

    # Username validation
    def clean_username(self):
        username = self.cleaned_data["username"]
    # Successfull username is at least 3 characters long
        if len(username) < 3:
            raise forms.ValidationError(
                "Username must be at least 3 characters long.")
    # Username can contains only letters, numbers and underscored
        if not re.match(r"^[A-Za-z0-9_]+$", username):
            raise forms.ValidationError(
                "Username can only contain letters, numbers, and underscores.")
    # check if user already exists
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    # Email validation
    # https://medium.com/@python-javascript-php-html-css/implementing-email-validation-in-django-projects-e210d4777fac
    def clean_email(self):
        email = self.cleaned_data["email"]

        # Block disposable domains
        blocked_domains = ["tempmail.com",
                           "mailinator.com", "10minutemail.com"]
        domain = email.split("@")[-1]
        if domain in blocked_domains:
            raise forms.ValidationError(
                "Disposable email addresses are not allowed.")

        # Check for duplication of emails
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")

        return email

    # Validation of age
    # https://docs.python.org/3/library/datetime.html
    def clean_dob(self):
        dob = self.cleaned_data["dob"]
        today = date.today()

        # Future date check FIRST
        if dob > today:
            raise forms.ValidationError(
                "Date of birth cannot be in the future.")

        # Calculate age - (today date - provided date in the form)
        age = today.year - dob.year - \
            ((today.month, today.day) < (dob.month, dob.day))

        # Too young
        if age < 18:
            raise forms.ValidationError(
                "You must be at least 18 years old to register.")

        # Too old (your rule)
        if age > 99:
            raise forms.ValidationError("Please enter a valid date of birth.")

        return dob

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',
                  'dob')

    # Creates the related profile immediately after the user is saved
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                dob=self.cleaned_data['dob'],
            )
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150, widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label="Password", strip=False, widget=forms.PasswordInput)


# Story form - to create and edit the story

class StoryForm(forms.ModelForm):
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        required=True,
        empty_label="Select a genre"
        )

    class Meta:
        model = Story
        fields = ['title', 'content', 'genre']
        widgets = {
            'title': forms.TextInput(attrs={
                'id': 'story-title',
                'class': 'story-title-input',
                'placeholder': 'Enter your story title here',
                'maxlength': 255,
                'aria-label': 'Story title input',
            }),
            'content': forms.Textarea(attrs={
                'id': 'story-text',
                'class': 'story-textarea',
                'placeholder': 'Write here (2,000 characters limit)',
                'maxlength': 2000,
                'rows': 10,
                'aria-label': 'Story content input',
            }),
            'genre': forms.Select(attrs={
                    'id': 'story-genre',
                    'class': 'story-genre-select',
                    'aria-label': 'Story genre select',
                    }),
        }

# Comment form - to create and edit the comment


class CommentForm(forms.ModelForm):
    author_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'comment-author-input',
            'placeholder': 'Your name',
            'maxlength': 255,
            'aria-label': 'Comment author name input',
        })
    )
    comment_text = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'id': 'comment-text',
            'class': 'comment-textarea',
            'placeholder': 'Write your comment here (500 characters limit)',
            'maxlength': 500,
            'rows': 5,
            'aria-label': 'Comment text input',
        })
    )
    rating = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=5,
        # Hidden input for rating, it will be set by JavaScript
        # when the user clicks on the stars
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Comment
        fields = ['author_name', 'comment_text', 'rating']
