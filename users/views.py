from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth.models import User

@login_required
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Set the user as a superuser
            user.is_superuser = True
            user.is_staff = True
            user.save()

            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Your account has been created! You are now able to log in as a superuser')
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})




def register1(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Set the user as a superuser
            user.is_superuser = True
            user.is_staff = True
            user.save()

            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Your account has been created! You are now able to log in as a superuser')
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def registerstaff(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Set the user as a superuser
            user.is_superuser = False
            user.is_staff = True
            user.save()

            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Your account has been created! You are now able to log in as a superuser')
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    print(request.user.profile.image.url)
    return render(request, 'users/profile.html', context)


