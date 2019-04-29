"""project_database URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from API_proj2app.views import *


# Fairly standard url requests

urlpatterns = [
    path('', index.default),
    path('admin/', admin.site.urls),
    path('<str:user_id>/poi', userInfo.aoi, name='poi'),
    path('users/', userInfo.users, name = "users"),
    path('users/<int:user_id>', userInfo.modifyUser, name="modifyUser"),
    path('locations/',userInfo.locations, name = "locations"),
    path('locations/<int:user_id>/<str:placeTitle>', userInfo.modifyLocation, name = "modifyLocation")
]
