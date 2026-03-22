from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.hashers import make_password
from .models import Profile

class SignUpForm(UserCreationForm):
    # User table - add email
    email = forms.EmailField(required=True)
    # Profile table - add dob, security question and answer - only to reset the password purpuse
    dob = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
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
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2','dob','security_question','security_answer')
    
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
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput)