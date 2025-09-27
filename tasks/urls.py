"""
URL configuration for tasks app
"""
from django.urls import path
from . import views

urlpatterns = [
    # API endpoints
    path('api/tasks/', views.create_task, name='create_task'),
    path('api/tasks/list/', views.get_tasks, name='get_tasks'),
    path('api/tasks/<int:task_id>/', views.get_task, name='get_task'),
    path('api/tasks/<int:task_id>/update/', views.update_task, name='update_task'),
    path('api/tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    
    # Template views
    path('', views.task_list_view, name='task_list'),
    path('add/', views.add_task_view, name='add_task'),
]
