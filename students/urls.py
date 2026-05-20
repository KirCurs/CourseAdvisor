from django.urls import path

from .views import interest_test

urlpatterns = [
    path("test/", interest_test, name="interest_test"),
]
