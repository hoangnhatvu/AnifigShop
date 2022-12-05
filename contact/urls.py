from django.urls import path
from . import views

urlpatterns = [
    path('', views.ContactView, name='contact'),
]