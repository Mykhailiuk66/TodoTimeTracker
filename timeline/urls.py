from django.urls import path
from . import views

urlpatterns = [
    path('', views.timelines, name='timeline'),
    path('create-timeline/', views.create_timeline, name='create-timeline'),
    path('update-timeline/<str:pk>', views.update_timeline, name='update-timeline'),
    path('delete-timeline/<str:pk>', views.delete_timeline, name='delete-timeline'),
    
    path('start-timeline/<str:pk>', views.start_timeline, name='start-timeline'),
    path('stop-timeline/<str:pk>', views.stop_timeline, name='stop-timeline'),
    
]
