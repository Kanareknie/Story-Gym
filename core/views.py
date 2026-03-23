from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from .forms import SignUpForm, LoginForm
import json
import random
from pathlib import Path



# Create your views here.

# Home page view
def home(request):
    return render(request, 'core/index.html')

# Sign up view
def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'core/register.html', {'form': form})

# Custom login view using our LoginForm
class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    authentication_form = LoginForm

# Custom logout view (can be extended if needed)
class CustomLogoutView(LogoutView):
    pass

# Randomizer - pull data from JSON - getting the random words from each cathegory.
def randomizer_view(request):
    # Gets current remporary words if they exist
    words = request.session.get('random_words')
    
    # When user clicks Start or Draw again, Django generates new words
    if request.method == 'POST':
        json_path = Path(__file__).resolve().parent.parent / 'docs' / 'randomizer.json'

        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Picks the random values in Python, on the server side
        words = {
            'main_character': random.choice(data['main_character']),
            'personality': random.choice(data['personality']),
            'physical_description': random.choice(data['physical_description']),
            'verb': random.choice(data['verb']),
            'place': random.choice(data['place']),
            'random_noun': random.choice(data['random_noun']),
        }

        # Stores words temporarily
        request.session['random_words'] = words

    return render(request, 'randomizer/randomizer.html', {'words': words})