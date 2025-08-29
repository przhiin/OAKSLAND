from django.urls import path
from .views import (
    LoginRequest,
    RegisterRequest,
    LogoutView,
    ViewProfile,
    UpdateProfile,
    SuperuserLogin,
)

urlpatterns = [
    path("login/", LoginRequest.as_view(), name="login"),
    path("register/", RegisterRequest.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/view/", ViewProfile.as_view(), name="view_profile"),
    path("profile/update/", UpdateProfile.as_view(), name="update_profile"),
    path("superuser/login/", SuperuserLogin.as_view(), name="superuser_login"),
]
