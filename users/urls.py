# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 22:17:05 2021

@author: Will
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import TemplateView
from .forms import UserLoginForm


app_name = 'users'
urlpatterns = [
    # Include default auth urls
    path('login/', auth_views.LoginView.as_view(template_name="registration/login.html",
                                                authentication_form=UserLoginForm), name='login'),
    path('register/',views.register,name='register'),
    path('activate/<slug:uidb64>/<slug:token>)/',
         views.activate, name='activate'),
    path('registered/',views.registered,name='registered'),
    path('profile/', views.profile, name='profile'),
    
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html"),name='password_reset'),
    
    
    ]