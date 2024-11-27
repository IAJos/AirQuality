"""
URL configuration for airQuality project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from airQualityApp import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/dashboard/', permanent=True)),
    path('admin/', admin.site.urls),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('data/', views.data, name='data'),
    path('data_last/', views.get_last_data, name='data_gas_ten'),
    path('get_devices_by_user/<int:User_id>/', views.get_devices_by_user, name='device_by_user'),
    path('get_data_by_device/<str:device_name_id>/', views.get_data_by_device, name='get_data_by_device'),
    path('chart/', views.chart_view, name='chart'),
    path('chart-gaz/', views.chart_data_gaz, name='chart_gaz'),
    path('chart-fine-particle/', views.chart_fine_particle, name='chart_fine_particle'),
    path('not-found/', views.no_found, name='404'),
]
