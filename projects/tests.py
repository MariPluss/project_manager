
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from .models import Project, Task


User = get_user_model()


class ProjectPermissionTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.admin = User.objects.create_user(
            username='test_admin',
            email='admin@example.com',
            password='TestPass123!',
            role='admin'
        )

        self.manager = User.objects.create_user(
            username='test_manager',
            email='manager@example.com',
            password='TestPass123!',
            role='manager'
        )

        self.user = User.objects.create_user(
            username='test_regular',
            email='user@example.com',
            password='TestPass123!',
            role='user'
        )

        self.project = Project.objects.create(
            name='Тестовый проект',
            description='Проект для проверки прав',
            owner=self.admin
        )

        self.task = Task.objects.create(
            project=self.project,
            title='Тестовая задача',
            assigned_to=self.user
        )

    def test_admin_can_create_project(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.post(
            '/api/projects/',
            {'name': 'Новый проект'},
            format='json'
        )

        self.assertEqual(response.status_code, 201)

    def test_manager_cannot_create_project(self):
        self.client.force_authenticate(user=self.manager)

        response = self.client.post(
            '/api/projects/',
            {'name': 'Новый проект'},
            format='json'
        )

        self.assertEqual(response.status_code, 403)

    def test_manager_can_create_task(self):
        self.client.force_authenticate(user=self.manager)

        response = self.client.post(
            '/api/projects/tasks/',
            {
                'project': self.project.id,
                'title': 'Задача менеджера'
            },
            format='json'
        )

        self.assertEqual(response.status_code, 201)

    def test_user_cannot_create_task(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            '/api/projects/tasks/',
            {
                'project': self.project.id,
                'title': 'Запрещённая задача'
            },
            format='json'
        )

        self.assertEqual(response.status_code, 403)

    def test_user_can_complete_own_task(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            f'/api/projects/tasks/{self.task.id}/',
            {'status': 'completed'},
            format='json'
        )

        self.assertEqual(response.status_code, 200)

        self.task.refresh_from_db()
        self.assertEqual(self.task.status, 'completed')

    def test_user_cannot_change_task_title(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            f'/api/projects/tasks/{self.task.id}/',
            {'title': 'Изменённое название'},
            format='json'
        )

        self.assertEqual(response.status_code, 403)

    def test_user_can_view_projects(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/projects/')

        self.assertEqual(response.status_code, 200)

    def test_manager_cannot_delete_project(self):
        self.client.force_authenticate(user=self.manager)

        response = self.client.delete(
            f'/api/projects/{self.project.id}/'
        )

        self.assertEqual(response.status_code, 403)
