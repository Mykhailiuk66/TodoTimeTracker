from django.urls import path
from . import views

urlpatterns = [
    path('', views.tasks, name='todo'),
    path('create-task/', views.create_task, name='create-task'),
    path('update-task/<str:pk>', views.update_task, name='update-task'),

    path('task-done/<str:pk>', views.task_done, name='task-done'),
    path('task-delete/<str:pk>', views.delete_task, name='task-delete'),
    
    path('create-tag/', views.create_tag, name='create-tag'),
    path('update-tag/', views.update_tag, name='update-tag'),
    path('delete-tag/', views.delete_tag, name='delete-tag'),
    
]