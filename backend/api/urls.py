from django.urls import path
from . import views

urlpatterns = [
    path('test_get/site=<int:site>/lookup-word=<str:lookup_word>/min-price=<int:min_price>/max-price=<int:max_price>', views.test, name='test_get'),
]