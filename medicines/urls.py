"""
URL configuration for medicines project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from medicines import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('medicine/index', views.index),
    path('medicine/create', views.create),
    path('medicine/update/<int:pk>/', views.update),
    path('medicine/delete/<int:pk>/', views.delete),
    path('medicine/getByID/<int:pk>/', views.getByID),
    path('medicine/status_medicine_create', views.status_medicine_create),
    path('accounts/', include('accounts.urls')),
    path('category/create', views.createCategory),
    path('category/get/<int:pk>', views.category_with_medicines),
    path('category/search/<str:name>', views.category_search_by_name),
]
