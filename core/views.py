from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from .forms import SignUpForm, LoginForm, StoryForm
import json
import random
from pathlib import Path
from django.contrib import messages
from .models import RandomizerResult, Story, Comment
from .forms import CommentForm
from django.utils.html import format_html
from django.urls import reverse


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
            messages.success(
                request, "Account created successfully. Welcome to Story Gym.")
            login(request, user)
            # If there are random words in the session and user click "Write Now", save them for the user and redirect to My Story page
            if request.session.get('random_words') and request.session.get('pending_write_now'):
                save_random_words_for_user(request, user)
                request.session.pop('pending_write_now', None)
                return redirect('my_story')

            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'core/register.html', {'form': form})

# Custom login view using our LoginForm


class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    authentication_form = LoginForm
    # Override form_valid to check for random words in the session and save them for the user if they exist

    def form_valid(self, form):
        response = super().form_valid(form)

        if self.request.session.get('random_words') and self.request.session.get('pending_write_now'):
            save_random_words_for_user(self.request, self.request.user)
            self.request.session.pop('pending_write_now', None)
            return redirect('my_story')

        return response

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
        json_path = Path(__file__).resolve().parent.parent / \
            'docs' / 'randomizer.json'

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
    # Clear the random words from the session after saving to the database
    request.session.pop('random_words', None)
    request.session.pop('pending_write_now', None)

    return randomizer_result

# Randomizer - step 3 - Redirects to My Story page if user is authenticated, otherwise to login page


def write_now_view(request):
    words = request.session.get('random_words')
    # temporary to test
    print("WRITE NOW VIEW CALLED")

    if not words:
        messages.error(request, "Please generate a prompt first.")
        return redirect('randomizer')
    # Sets a flag in the session to indicate that the user has clicked "Write Now" and is pending redirection to My Story page after login
    request.session['pending_write_now'] = True

    if request.user.is_authenticated:
        save_random_words_for_user(request, request.user)
        request.session.pop('pending_write_now', None)
        return redirect('my_story')

    return redirect('login')

# My Story page view

# Add login requiremnt to My Story page - if user is not authenticated, redirect to login page. After login, if there are random words in the session and user click "Write Now", save them for the user and redirect to My Story page


@login_required
def my_story_view(request):
    randomizer_result_id = request.session.get('current_randomizer_result_id')
# If there are no random words or user is not authenticated, redirect to randomizer page with an error message
    if not randomizer_result_id:
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
    if request.method == 'POST':
        print("POST request received in my_story_view")
        # clear button
        if 'clear_story' in request.POST:
            form = StoryForm()
            return render(
                request,
                'stories/my_story.html',
                {
                    'form': form,
                    'prompt_words': randomizer_result.words,
                }
            )

        form = StoryForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            # save for later = draft
            if 'save_draft' in request.POST:
                story = Story.objects.create(
                    user=request.user,
                    randomizer=randomizer_result,
                    title=title,
                    content=content,
                    status=0,
                )
                # Use reverse to get the URL of the account page and include it in the success message
                # https://docs.bearer.com/reference/rules/python_django_mark_safe/
                account_url = reverse('account')

                messages.success(
                    request,
                    format_html(
                        'Your story was saved as a draft. <a href="{}">Go to your account</a>',
                        account_url
                    )
                )
                return redirect('home')

            # publish
            if 'publish_story' in request.POST:
                story = Story.objects.create(
                    user=request.user,
                    randomizer=randomizer_result,
                    title=title,
                    content=content,
                    status=1,
                )

                # Use reverse to get the URL of the account page and include it in the success message
                # https://docs.bearer.com/reference/rules/python_django_mark_safe/
                story_url = reverse('preview_story', args=[story.id])

                messages.success(
                    request,
                    format_html(
                        'Your story has been published! <a href="{}">View your story →</a>',
                        story_url
                    )
                )
                return redirect('home')

    else:
        form = StoryForm()

    # Render the My Story page with the random words from the database
    return render(
        request,
        'stories/my_story.html',
        {
            'form': form,
            'prompt_words': randomizer_result.words
        }
    )


# Preview Story page view to be viewed after publishing the story, with a unique URL for each story.

def preview_story_view(request, story_id):
    story = get_object_or_404(Story, id=story_id, status=1)  # Only published stories can be previewed
    comments = story.comments.all()  # Get all comments for the story
    
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)

            comment.story = story

            if request.user.is_authenticated:
                comment.user = request.user
                comment.author_name = request.user.username

            
            
            elif not comment.author_name:
                form.add_error('author_name', 'Please enter your name to post a comment.')
                return render(request, 'stories/preview_story.html', {
                    'story': story,
                    'comments': comments,
                    'comment_form': form,
                })
            
            comment.save()
            messages.success(request, "Comment added successfully.")
            return redirect('preview_story', story_id=story.id)
    else:
        form = CommentForm()
        
        

    return render(request, 'stories/preview_story.html', {
        'story': story,
        'comments': comments,
        'comment_form': form,
    })

# Edit Story page view - only the author of the story can edit it. If another user tries to access the URL, they will see a 404 page not found error.
@login_required
def edit_story_view(request, story_id):
    story = get_object_or_404(Story, id=story_id, user=request.user )  # Only the author can edit the story

    if request.method == 'POST':
        if 'clear_story' in request.POST:
            form = StoryForm(instance=story)
            return render(request, 'stories/my_story.html', {
                'form': form,
                'story': story,
                'prompt_words': story.randomizer.words,
                'is_editing': True,  # Flag to indicate that we are editing an existing story
            })
            
        form = StoryForm(request.POST, instance=story)

    # If the form is valid, save the changes but set the status to 0 (not published) so the user can review the changes before publishing again. If the user clicks "Publish" button, set the status to 1 (published) and redirect to the preview story page.
        if form.is_valid():
            updated_story = form.save(commit=False)
            
            if 'save_draft' in request.POST:
                updated_story.status = 0  # Set status to not published yet, so the user can review the changes before publishing again
                updated_story.save()
                messages.success(request, "Your story has been updated.")
                return redirect('account')
        
            if 'publish_story' in request.POST:
                updated_story.status = 1 # Set status to published
                updated_story.save()
                messages.success(request, "Your story has been updated and published.")
                return redirect('preview_story', story_id=updated_story.id)
    else:
        form = StoryForm(instance=story)

    return render(request, 'stories/my_story.html', {
        'form': form,
        'story': story,
        'prompt_words': story.randomizer.words,
        'is_editing': True,  # Flag to indicate that we are editing an existing story
    })

# Delete Story view - only the author of the story can delete it. If another user tries to access the URL, they will see a 404 page not found error. After deleting the story, redirect to the account page with a success message.
@login_required
def delete_story_view(request, story_id):
    story = get_object_or_404(Story, id=story_id, user=request.user)  # Only the author can delete the story

    if request.method == 'POST':
        story.delete()
        messages.success(request, "Your story has been deleted.")
        return redirect('account')

    return redirect('account') 

# Repository page view

def repo_view(request):
    published_stories = Story.objects.filter(status=1).select_related('user', 'randomizer').order_by('-created_on')
    # Get the latest published story to feature it at the top of the repository page
    latest_story = published_stories.first()
    
    context = {
        'latest_story': latest_story,
        'stories': published_stories,
    }
    
    return render(request, 'stories/repo.html', context)


# Account page view

@login_required
def account_view(request):
    user_stories = Story.objects.filter(user=request.user).select_related('randomizer').order_by('-created_on')
    # Get the latest story of the user to feature it at the top of the account page
    latest_user_story = user_stories.first()
    
    context = {
        'latest_user_story': latest_user_story,
        'user_stories': user_stories,
    }
    
    return render(request, 'accounts/account.html', context)
