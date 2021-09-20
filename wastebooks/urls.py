from django.urls import path
from . import views

app_name = 'wastebooks'

urlpatterns = [
    # HEERF 
    path('heerf/', views.heerf, name='heerf'),
    path('heerf-state/', views.heerf_state, name='heerf_main'),
    path('heerf-inst/', views.heerf_inst, name='heerf_lookup'),
    path('svog/', views.svog, name='svog'),
    path('svog_state/', views.svog_state, name='svog_state'),
    path('svog_city/', views.svog_city, name='svog_city'),
    path('svog_venue/', views.svog_venue, name='svog_venue'),
    ]
