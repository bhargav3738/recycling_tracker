from django.urls import path
from django.contrib.auth import views as auth_views
from tracker_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('statistics/', views.statistics, name='statistics'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]