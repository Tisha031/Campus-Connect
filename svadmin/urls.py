from django.urls import path
from . import views

urlpatterns = [
    path('', views.svadmin, name='svadmin'),
    path('generatestaff', views.generatestaff, name='generatestaff'),
    path('emailcontent', views.emailcontent, name='emailcontent'),
    path('allstudents', views.allstudents, name='allstudents'),
    path('testresults', views.test_results, name='testresults'),
    path('student/<str:username>/', views.student_detail, name='student_detail'), 
    path('company', views.company, name='company'),
    path('company/<int:id>/', views.company_detail, name='company_detail'),
]