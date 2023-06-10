"""
URL configuration for meaty_bangkit project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from meaty_app.views import user_register, user_login, upload_image, user_upload_history


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', user_register, name='user-register'),
    path('api/login/', user_login, name='user-login'),
    path('api/upload/', upload_image, name='upload-image'),
    path('api/history/<int:user_id>/', user_upload_history, name='user-upload-history'),
]
