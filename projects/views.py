
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied

from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from .permissions import IsProjectRolePermission


# Список проектов и создание проекта
class ProjectListAPIView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsProjectRolePermission]

    def get_queryset(self):
        return Project.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# Просмотр, изменение и удаление проекта
class ProjectDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsProjectRolePermission]

    def get_queryset(self):
        return Project.objects.all()


# Список задач и создание задачи
class TaskListAPIView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsProjectRolePermission]

    def get_queryset(self):
        return Task.objects.all()

    def perform_create(self, serializer):
        if self.request.user.role not in ['admin', 'manager']:
            raise PermissionDenied(
                "У вас нет прав на создание задач."
            )

        serializer.save()


# Просмотр, изменение и удаление задачи
class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsProjectRolePermission]

    def get_queryset(self):
        return Task.objects.all()

    def perform_update(self, serializer):
        user = self.request.user

        if user.role in ['admin', 'manager']:
            serializer.save()
            return

        if user.role == 'user':
            changed_fields = set(serializer.validated_data.keys())

            if changed_fields != {'status'}:
                raise PermissionDenied(
                    "Вы можете изменять только статус задачи."
                )

            if serializer.validated_data['status'] != 'completed':
                raise PermissionDenied(
                    "Вы можете только завершать задачи."
                )

            if serializer.instance.assigned_to_id != user.pk:
                raise PermissionDenied(
                    "Вы можете завершать только назначенные вам задачи."
                )

            serializer.save()
            return

        raise PermissionDenied(
            "У вас нет прав на изменение задачи."
        )
