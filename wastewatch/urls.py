"""
URL configuration for wastewatch project.

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
from .views import main_page, logout, view_report, AdminUserView
from django.urls import path, include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls, name='admin_url'),
    path('accounts/', include('allauth.urls')),
    path('accounts/logout', logout, name='logout'),
    path('', main_page, name='main_page'),
    path('report/', views.submit_report, name='upload_file'),
    path('report/success/', views.report_success, name='upload_success'),
    path('view-reports/<int:question_id>', views.view_report, name='view_report'),
    path('report_resolved_success/', views.report_resolved_success, name='report_resolved_success'),
    path('my_reports/', views.my_reports, name='my_reports'),
    path('view_my_report/<int:report_id>', views.view_my_report, name='view_my_report'),
    path('view_admin_page/', AdminUserView.as_view(), name='admin_page')
]

