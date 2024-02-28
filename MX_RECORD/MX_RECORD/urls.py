"""
URL configuration for MX_RECORD project.

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
from myapp import views


urlpatterns = [
    path("", views.LoginPage, name="login"),
    path("searchresult/", views.search_results, name="search_results"),
    path("logout/", views.logout_view, name="logout"),
    path("admin/", admin.site.urls),
    path("import-file/", views.import_file, name="import-file"),
    path("states/<str:country_name>/", views.get_states, name="get_states_by_country"),
    path("delete/", views.delete, name="delete"),
    path('dashboard/', views.get_dashboard, name='dashboard'),
    path('mxrecords/', views.get_records, name='mxrecords'),
    path(
        "delete/unverified/",
        views.delete_all_unverified_data,
        name="delete_all_unverified_data",
    ),
    path(
        "delete/domain-not-live/",
        views.delete_all_domain_not_live_data,
        name="delete_all_domain_not_live_data",
    ),
    path(
        "delete/live-no-mx/",
        views.delete_all_domain_live_no_mx_data,
        name="delete_all_domain_live_no_mx_data",
    ),
    path(
        "delete/verified/",
        views.delete_all_verified_data,
        name="delete_all_verified_data",
    ),
]
