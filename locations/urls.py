from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('offline_view/', views.offline, name='offline'),
    path('signup/', views.signup, name='signup'),
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('email/', views.begin_emailing, name='begin_emailing'),
    path('update/', views.begin_update, name='begin_update'),
    path('update9923/', views.update, name='update'),
    path('email4497/', views.email, name='email'),
]
