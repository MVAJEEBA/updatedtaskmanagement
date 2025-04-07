from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model 

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')

    # Override the groups and user_permissions fields to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Custom related name
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='customuser',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Custom related name
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser',
    )

    

class Project(models.Model):
    STATUS_CHOICES = (
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    created_by =  models.TextField(max_length=50,null=True, blank=True)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='assigned_managers')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def is_active(self):
        return self.status == 'in_progress'

    def is_completed(self):
        return self.status == 'completed'

    def is_upcoming(self):
        return self.start_date > timezone.now().date()

    def is_overdue(self):
        return self.end_date < timezone.now().date() and not self.is_completed()


class Statuses(models.Model):
    status_type=models.CharField(max_length=50)

class Task(models.Model):
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )

    
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=255)
    created_by =  models.TextField(max_length=50,null=True, blank=True)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.ForeignKey(Statuses, on_delete=models.CASCADE,null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks',null=True, blank=True, )
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to='task_files/', null=True, blank=True)


    def __str__(self):
        return self.name

    def is_high_priority(self):
        return self.priority == 'high'

    def is_completed(self):
        return self.status == 'completed'

from django.db import models
from django.conf import settings



from django.db import models
from django.conf import settings
from django.utils import timezone

class EmployeePerformanceReport(models.Model):
    employee = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE, 
        related_name='performance_reports'
    )
    report_date = models.DateField(default=timezone.now)
    tasks_completed = models.PositiveIntegerField(default=0)
    total_hours_worked = models.PositiveIntegerField(default=0)
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Performance Report for {self.employee} on {self.report_date}"

    

    def generate_report(self):
        """
        Generate a performance report (e.g., summary of tasks completed and hours worked).
        """
        return f"Employee: {self.employee.username}\nTasks Completed: {self.tasks_completed}\nHours Worked: {self.total_hours_worked}\nFeedback: {self.feedback if self.feedback else 'No feedback'}"

# # # models.py



class WorkLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='worklogs',null =True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)  # Reference to Task model
    date = models.DateField()
    hours = models.PositiveIntegerField()
    description = models.TextField()

    def __str__(self):
        return f"WorkLog for {self.employee} on {self.date}"

    class Meta:
        unique_together = ('user', 'task', 'date')  # Ensure a user doesn't log more than one entry per day for the same task.




