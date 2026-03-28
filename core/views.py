from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from .forms import SignUpForm, LoginForm
import json
import random
from pathlib import Path
from django.contrib import messages
from .models import RandomizerResult



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
            messages.success(request, "Account created successfully. Welcome to Story Gym.")
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

# Randomizer - step 1 - pull data from JSON - getting the random words from each cathegory.
# Used https://python.plainenglish.io/how-to-read-json-file-in-python-with-examples-in-2026-9877d0cdca71

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

# Randomizer - step 2 -  decides what happens after clicking Write Now button

def save_random_words_for_user(request, user):
    words = request.session.get('random_words')

    if not words:
        return None

    randomizer_result = RandomizerResult.objects.create(
        user=user,
        words=words
    )

    request.session['current_randomizer_result_id'] = randomizer_result.id
    del request.session['random_words']

    return randomizer_result

#Randomizer - step 3 - Redirects to My Story page if user is authenticated, otherwise to login page
def write_now_view(request):
    words = request.session.get('random_words')

    if not words:
        messages.error(request, "Please generate a prompt first.")
        return redirect('randomizer')

    if request.user.is_authenticated:
        save_random_words_for_user(request, request.user)
        return redirect('my_story')

    return redirect('login')

# My Story page view

def my_story_view(request):
    randomizer_result_id = request.session.get('current_randomizer_result_id')
# If there are no random words or user is not authenticated, redirect to randomizer page with an error message
    if not randomizer_result_id or not request.user.is_authenticated:
        messages.error(request, "Please generate a prompt first.")
        return redirect('randomizer')
    # Fetch the randomizer result from the database using the stored ID and ensure it belongs to the current user
    try:
        randomizer_result = RandomizerResult.objects.get(
            id=randomizer_result_id,
            user=request.user
        )
    # If the randomizer result does not exist or does not belong to the user, redirect to randomizer page with an error message
    except RandomizerResult.DoesNotExist:
        messages.error(request, "Please generate a prompt first.")
        return redirect('randomizer')
    # Render the My Story page with the random words from the database
    return render(
        request,
        'stories/my_story.html',
        {'prompt_words': randomizer_result.words}
    )


# Preview Story page view

def preview_story_view(request):
    return render(request, 'stories/preview_story.html')


# Repository page view

def repo_view(request):
    return render(request, 'stories/repo.html')


# Account page view

def account_view(request):
    return render(request, 'accounts/account.html')
