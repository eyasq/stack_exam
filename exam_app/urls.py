"""
URL configuration for stack_exam project.

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
from django.urls import include, path

from exam_app import views

urlpatterns = [
    path('', views.index),
    path('post_register', views.post_register),
    path('post_login', views.post_login),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('add_pie', views.add_pie),
    path('pies', views.all_pies),
    path('pies/<int:pie_id>', views.show_pie),
    path('vote/<int:pie_id>', views.vote_pie),
    path('remove_vote', views.remove_vote),
    path('pies/edit/<int:pie_id>', views.edit_pie),
    path('edit_pie', views.post_edit_pie),
    path('delete/<int:pie_id>', views.delete)
]
