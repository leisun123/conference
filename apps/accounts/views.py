#coding:utf8
from django.contrib.auth.models import Group
from django.shortcuts import render, HttpResponse
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
            if user is not None:
                auth_login(request, user)
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


@csrf_protect
@login_required
def password(request):
    user = request.user

    if request.method == "POST":
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            data = form.clean()
            if user.check_password(data["old_password"]):
                user.set_password(data["password"])
                user.save()
                messages.success(request, "新密码设置成功！请重新登录")
                auth_logout(request)
                return HttpResponseRedirect(reverse("login"))
            else:
                messages.error(request,'当前密码输入错误')
                return render(request, "/registration/registration.html",
                              {'form': form,
                               'errors': form.errors,
                               'title':'Change Password'})
    else:
        form = PasswordChangeForm()

    return render(request, "registration/password.html",
                  {'form': form,
                   'title': 'Change Password'})

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


