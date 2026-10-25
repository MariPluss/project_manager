from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from .forms import RegisterForm
from projects.models import Project, Task, Comment
from projects.forms import CommentForm
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# Регистрация пользователя
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            group, created = Group.objects.get_or_create(
                name='User'
            )
            user.groups.add(group)

            messages.success(
                request,
                'Регистрация прошла успешно! Теперь войдите в систему.'
            )

            return redirect('login')

    else:
        form = RegisterForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )


# Главная страница пользователя
@login_required
@user_passes_test(
    lambda user: user.role in ['admin', 'manager', 'user']
    )
def home(request):

    # Проекты текущего пользователя
    projects = Project.objects.filter(
        owner=request.user
    )

    # Задачи из проектов текущего пользователя
    tasks = Task.objects.filter(
        project__owner=request.user
    )

    return render(
        request,
        'accounts/home.html',
        {
            'projects': projects,
            'tasks': tasks,
        }
    )

    # Добавление комментария к задаче
@login_required
def add_comment(request, task_id):
    task = get_object_or_404(
        Task,
        id=task_id
    )

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()

    return redirect('home')

    

class ManagerDashboardView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    TemplateView
):
    template_name = 'accounts/home.html'

    def test_func(self):
        return self.request.user.role in ['admin', 'manager']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        context['tasks'] = Task.objects.all()
        return context