"""to_do_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
# To Use the default Django's Login and Logout Views
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
# To use routers in REST Framework
from rest_framework import routers

from accounts.views import RegistrationView, AccountsView, EditAccountsView
from todo_core.sitemaps import StaticViewSitemap

# Importing the Views of users app for routing purpose

# Routes to the API Endpoint
router = routers.SimpleRouter()

sitemaps = {"static": StaticViewSitemap}


urlpatterns = [
    # Home Page - By default, loading the To-Do List
    path("", include("todo_core.urls")),
    path("admin/", admin.site.urls),
    # Routing to User Registration Page
    path("register/", RegistrationView.as_view(), name="register"),
    # The template_name = 'some path' tells django to look for the login page in 'users' -> 'templates' Directory
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="accounts/logout.html"),
        name="logout",
    ),
    # Including a EmailValidationOnForgotPassword class from users/forms.py - That tells the user that the entered
    # email during password reset is not a registered email (Not present in the system).
    path("profile/", AccountsView.as_view(), name="profile"),
    path("edit_profile/", EditAccountsView.as_view(), name="edit_profile"),
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
