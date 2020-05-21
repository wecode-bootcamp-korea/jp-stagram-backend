from django.urls import path, include
from account import views

urlpatterns = [
    path('sign-up', views.RegisterView.as_view(), name='account-register'),
    path('sign-in', views.LoginView.as_view(), name='account-login'),
    # path('/profile', views.ProfileView.as_view(), name='account-profile')
]
