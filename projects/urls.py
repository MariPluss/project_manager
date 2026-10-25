
from django.urls import path

from .views import (
    ProjectListAPIView,
    ProjectDetailAPIView,
    TaskListAPIView,
    TaskDetailAPIView,
)

urlpatterns = [
    path(
        '',
        ProjectListAPIView.as_view(),
        name='project-list'
    ),

    path(
        '<int:pk>/',
        ProjectDetailAPIView.as_view(),
        name='project-detail'
    ),

    path(
        'tasks/',
        TaskListAPIView.as_view(),
        name='task-list'
    ),

    path(
        'tasks/<int:pk>/',
        TaskDetailAPIView.as_view(),
        name='task-detail'
    ),
]
