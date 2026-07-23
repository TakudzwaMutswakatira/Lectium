"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from apps.users import views as user_views
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

def redirect_to_login(request):
    """Sends users hitting the root domain straight to the login page."""
    return redirect('login')

urlpatterns = [
    # 1. The Root Path
    path('', redirect_to_login, name="home"),

    # 2. Top-Level Auth & Admin Routes
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name="register"),
    path('profile/', user_views.profile, name="profile"),
    path('login/', auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html", next_page="login"), name="logout"),

    # 3. Modular App Routes (Clean browser URLs + Correct Python paths)
    #path('books/', include("apps.books.urls")),
    #path('clubs/', include("apps.clubs.urls")),
    #path('discussions/', include("apps.discussions.urls")),
    #path('events/', include("apps.events.urls")),
    
    # Note: We include users.urls here just in case you want to add 
    # other user-related paths later (like /users/settings/ or /users/<id>/)
    #path('users/', include("apps.users.urls")),
]
