from django.urls import path
from . import views

app_name = 'wastebooks'

urlpatterns = [
    # HEERF 
    path('heerf/', views.heerf, name='heerf'),
    path('heerf-state/', views.heerf_state, name='heerf_main'),
    path('heerf-inst/', views.heerf_inst, name='heerf_lookup'),

    ]
