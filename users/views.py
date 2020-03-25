from django.shortcuts import render,redirect
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Your account has been created! You are now able to login!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form':form})


def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.Files, instance=request.user)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Your Profile has been updated')
            return redirect('hostels')
    else:
        u_form = UserUpdateForm()
        p_form = ProfileUpdateForm()

    stuff_for_frontend = {
        'u_form':u_form,
        'p_form':p_form,
    }
    return render(request,'users/userprofile.html',stuff_for_frontend)
