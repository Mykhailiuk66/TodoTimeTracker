from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    
    
    path('edit-profile/', views.edit_profile, name='edit-profile')
    
]