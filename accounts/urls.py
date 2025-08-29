from django.urls import path
from . import views

urlpatterns = [
    # LOGIN
    path("login/request/", views.login_request, name="login_request"),
#new
  
    # Superuser login
    path("superuser-login/", views.superuser_login, name="superuser_login"),

    
    # REGISTER
    path("register/request/", views.register_request, name="register_request"),

    #profile
    path("profile/", views.view_profile, name="view_profile"),
    path("profile/update/", views.update_profile, name="update_profile"),

    path("logout/", views.logout_view, name="logout"),
    path('login/superuser/', views.superuser_login, name='superuser_login'),
]
