from django.urls import path
from . import views

urlpatterns = [
    path('', views.staff, name='staff'),
    path('filterstudents/', views.staff, name='filterstudents'),
    path('viewcompanydetails/', views.viewcompanydetails, name='viewcompanydetails'),
]
