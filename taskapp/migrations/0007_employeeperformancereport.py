# Generated by Django 4.2.20 on 2025-04-08 09:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('taskapp', '0006_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeePerformanceReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_date', models.DateField(default=django.utils.timezone.now)),
                ('tasks_completed', models.PositiveIntegerField(default=0)),
                ('total_hours_worked', models.PositiveIntegerField(default=0)),
                ('feedback', models.TextField(blank=True, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='performance_reports', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
