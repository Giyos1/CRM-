from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='user-logout'),
    path('session/', views.SessionUserView.as_view(), name='session'),
]
