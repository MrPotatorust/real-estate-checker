from django.urls import path
from . import views

urlpatterns = [
    path('test_get/', views.test, name='test_get'),
]