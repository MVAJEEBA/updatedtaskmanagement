from django.contrib import admin
from django.urls import include, path
from .import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [

    path('login/', views.loginpage, name='loginpage'), 
    path('registration/',views.registration,name='registration'),
    path('logout/',views.logout, name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manager_dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    # path('task_assignment/', views.task_assignment, name='task_assignment'),
   
    path('create_project/', views.create_project, name='create_project'),
    path('create_task/<int:id>/', views.create_task, name='create_task'),
    path('project_list/', views.project_list, name='project_list'),
    path('task_list/', views.task_list, name='task_list'),
   
   path('user/<int:user_id>/', views.user_detail, name='user_detail'),
   path('work_log/',views.work_log_view, name = 'work_log'),
    path('do-task/<int:id>/', views.do_task, name='do_task'),
    path('statustype/',views.statustype,name='statustype'),
    path('update_staus/', views.update_staus, name='update_staus'),
    path('performance_report/<str:username>/', views.performance_report, name='performance_report'),
    path('performance_reportview/',views.performance_reportview,name='performance_reportview')

]