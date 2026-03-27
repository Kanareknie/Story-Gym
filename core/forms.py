from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.hashers import make_password
from .models import Profile
import re


class SignUpForm(UserCreationForm):
    # User table - add email
    email = forms.EmailField(required=True)
    # Profile table - add dob, security question and answer - only to reset the password purpuse
    dob = forms.DateField(
        required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    security_question = forms.ChoiceField(
        required=True,
        choices=[
            ('pet', 'What was the name of your first pet?'),
            ('school', 'What was the name of your first school?'),
            ('mother', "What is your mother's maiden name?"),
        ]
    )
    security_answer = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )

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
        blocked_domains = ["tempmail.com", "mailinator.com", "10minutemail.com"]
        domain = email.split("@")[-1]
        if domain in blocked_domains:
                raise forms.ValidationError(
                    "Disposable email addresses are not allowed.")
                
        # Check for duplication of emails
        if User.objects.filter(email=email).exists():
                raise forms.ValidationError("This email is already registered.")

        return email

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',
                  'dob', 'security_question', 'security_answer')

    # Creates the related profile immediately after the user is saved
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                dob=self.cleaned_data['dob'],
                security_question=self.cleaned_data['security_question'],
                # hashes the answer before storing it
                security_answer_hash=make_password(
                    self.cleaned_data['security_answer']
                )
            )
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150, widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label="Password", strip=False, widget=forms.PasswordInput)
