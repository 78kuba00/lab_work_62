from django.urls import path, include, re_path
from accounts.views import RegisterView, UserDetailView, UsersListView, UserChangeView, UserPasswordChangeView
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    # re_path(r'^login?/$', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/', RegisterView.as_view(), name='create'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='detail'),
    path('users/', UsersListView.as_view(), name='users'),
    path('change/', UserChangeView.as_view(), name='change'),
    path('password_change/', UserPasswordChangeView.as_view(), name='password_change')
]