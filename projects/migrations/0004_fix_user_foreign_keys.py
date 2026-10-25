from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_comment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.AlterField(
                    model_name='project',
                    name='owner',
                    field=models.ForeignKey(
                        to='auth.User',
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='projects',
                    ),
                ),
                migrations.AlterField(
                    model_name='project',
                    name='owner',
                    field=models.ForeignKey(
                        to=settings.AUTH_USER_MODEL,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='projects',
                    ),
                ),
                migrations.AlterField(
                    model_name='task',
                    name='assigned_to',
                    field=models.ForeignKey(
                        to='auth.User',
                        on_delete=django.db.models.deletion.SET_NULL,
                        null=True,
                        blank=True,
                        related_name='assigned_tasks',
                    ),
                ),
                migrations.AlterField(
                    model_name='task',
                    name='assigned_to',
                    field=models.ForeignKey(
                        to=settings.AUTH_USER_MODEL,
                        on_delete=django.db.models.deletion.SET_NULL,
                        null=True,
                        blank=True,
                        related_name='assigned_tasks',
                    ),
                ),
                migrations.AlterField(
                    model_name='comment',
                    name='author',
                    field=models.ForeignKey(
                        to='auth.User',
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='comments',
                    ),
                ),
                migrations.AlterField(
                    model_name='comment',
                    name='author',
                    field=models.ForeignKey(
                        to=settings.AUTH_USER_MODEL,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='comments',
                    ),
                ),
            ],
            state_operations=[],
        ),
    ]