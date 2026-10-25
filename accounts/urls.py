from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
        path(
        'manager/',
        views.ManagerDashboardView.as_view(),
        name='manager_dashboard'
    ),
    path('register/', views.register, name='register'),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='accounts/login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    path(
    'task/<int:task_id>/comment/',
    views.add_comment,
    name='add_comment'
),

]