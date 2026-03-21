from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from .forms import SignUpForm, LoginForm


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