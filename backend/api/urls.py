from django.urls import path
from . import views

urlpatterns = [
    path('test_get/<int:site>/<str:lookup_word>', views.test, name='test_get'),
]