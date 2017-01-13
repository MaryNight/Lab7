from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from lab7.models import *
from lab7.forms import *
from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,logout
from django.contrib import auth

# Create your views here.

class ExampleView(View):
    def get(self, request):
        return render(request, 'base.html')

class SuccessView(View):
    def get(self, request):
        return render(request, 'success.html')

class LessonsView(ListView):
    model = Lesson
    context_object_name = 'lessons'
    template_name = 'lessons.html'
    
    def get_queryset(self):
        qs = Lesson.objects.all().order_by('id')
        return qs

class LessonView(View):
    def get(self, request, id):
        data = Lesson.objects.get(id__exact=id)
        return render(request, 'lesson.html', {'lesson':data})

def registration_old(request):
    errors = []
    if request.method == 'POST':
        username = request.POST.get('username')
        if not username:
            errors.append('Login required')
        elif len(username)<5:
            errors.append('Login should be 5 or more symbols')
        
        password = request.POST.get('password')
        if not password:
            errors.append('Password required')
        elif len(password)<8:
            errors.append('Password length should be 8 or more')
        
        password_repeat = request.POST.get('password2')
        
        if password != password_repeat:
            errors.append('Password should be similar')
        #print(errors)
        if not errors:
            user_model = get_user_model()
            user = user_model.objects.create_user(username=username,
                                        email=request.POST.get('email'),
                                        password=password,
                                        first_name=request.POST.get('first_name'),
                                        last_name=request.POST.get('last_name'),
                                        )
            return HttpResponseRedirect('/lab7/success')
    return render(request, 'logon.html', {'errors': errors})

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/lab7/')
        return render(request, 'signup.html', {'form': form})
    else:
        form = RegistrationForm()
    return render(request, 'signup.html', {'form': form})

def authorization(request):
    redirect_url = '/lab7/success'
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data['login'],
                                     password=form.cleaned_data['password'])
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect(redirect_url)
            else:
                form.add_error(None, 'Wrong login or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form':form, 'continue': redirect_url})

@login_required
def exit(request):
    logout(request)
    return render(request, 'logout.html')
