from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("login", views.login_view, name="login"),
    path("upload", views.upload, name="upload"),
    path("signup", views.signup, name="signup"),
    path("logout", views.logout_view, name="logout"),
]