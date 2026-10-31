from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    
    # Student paths (using student_sessionid)
    path('student/register/', views.student_register, name='student_register'),
    path('student/login/', views.student_login, name='student_login'),
    path('student/logout/', views.student_logout, name='student_logout'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/ask/', views.ask_doubt, name='ask_doubt'),
    path('student/doubt/<int:doubt_id>/', views.student_doubt_detail, name='student_doubt_detail'),

    # Teacher paths (using teacher_sessionid)
    path('teacher/register/', views.teacher_register, name='teacher_register'),
    path('teacher/login/', views.teacher_login, name='teacher_login'),
    path('teacher/logout/', views.teacher_logout, name='teacher_logout'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/doubt/<int:doubt_id>/', views.teacher_doubt_detail, name='teacher_doubt_detail'),
]
