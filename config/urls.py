from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path
from django.contrib.auth import views as auth_views


def home(request):
    return render(request, "home.html")


urlpatterns = [
    path("", home, name="home"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("admin/", admin.site.urls),
    path("students/", include("students.urls")),
    path("recommendations/", include("recommendations.urls")),
]
