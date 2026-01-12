from django.urls import path
from . import views



urlpatterns = [
    path("", views.index, name='index'),
    path("login/", views.login, name='login'),

    path("logout/", views.logout, name='logout'),

    path("register/", views.register, name='register'),

    path("task_list",views.task_list, name='task_list'),

    path('take_task/<int:task_id>/', views.take_task, name='take_task'),

    path('change_status/<int:task_id>/', views.change_status, name='change_status'),

    path('tasks/create/', views.create_task, name='create_task'),

    path('tasks/edit/<int:task_id>/', views.edit_task, name='edit_task'),

    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete_task'),


]

