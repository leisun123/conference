#coding:utf8
from django.contrib.auth.models import Group
from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponsePermanentRedirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import LoginForm, RegisterForm, ChangeUserImageForm, PasswordChangeForm

# Create your views here.

@csrf_protect
def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            print(user)
            if user is not None:
                auth_login(request, user)
                if user.is_assigned_password:
                    user.is_assigned_password = False
                    user.save()
                    return HttpResponseRedirect(reverse('password_change'))
                    
                    
                return HttpResponseRedirect(reverse('index'))
        else:
            auth_logout(request)
            
            return render(request, 'registration/registration.html',
                          {'form': login_form,
                           'errors': login_form.errors,
                           'title': 'Sign In'})

    else:
        # request.session['next_url'] = request.GET.get('next')
        login_form = LoginForm()
    return render(request, 'registration/registration.html',
                  {'form': login_form,
                   'title': 'Sign In'})

@csrf_protect
def logout(request):
    auth_logout(request)
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    return HttpResponseRedirect(reverse('index'))

@csrf_protect
def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            Group.objects.get(name="scholar").user_set.add(user)
            if user is not None:
                user = authenticate(email=register_form.cleaned_data['email'],password=register_form.cleaned_data['password'])
                auth_login(request,user)
                return HttpResponseRedirect(reverse('index'))
        else:
            auth_logout(request)
            return render(request, 'registration/registration.html',
                          {'form': register_form,
                           'errors': register_form.errors,
                           'title':'Register'})
        
    else:
        register_form = RegisterForm()
        user = None
    return render(request, 'registration/registration.html',
                  {'form': register_form,
                   'title': 'Register'})


def updateImage(request):
    if request.method == 'POST':
        form = ChangeUserImageForm(request.POST,request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            user = request.user
            user.avatar = image
            user.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = ChangeUserImageForm()
    return render(request, 'registration/changeuserimage.html',{'form':form})


