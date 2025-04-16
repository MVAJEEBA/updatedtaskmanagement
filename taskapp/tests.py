from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from taskapp.models import Task, Project, Statuses, WorkLog  # Adjust to your actual app structure
from django.contrib.messages import get_messages
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
import json





class AdminDashboardTest(TestCase):

    def setUp(self):
     
        self.admin_user = CustomUser.objects.create_user(
            username='admin', password='adminpassword', email='admin@example.com', role='admin'
        )
        
       
        self.non_admin_user = CustomUser.objects.create_user(
            username='user', password='userpassword', email='user@example.com', role='user'
        )

        
        self.project1 = Project.objects.create(
            name='Project 1', start_date=date.today() 
        )
        self.project2 = Project.objects.create(
            name='Project 2', start_date=date.today()  
        )

        
        self.url = reverse('admin_dashboard')  # Adjust this URL name if necessary


class RegistrationViewTest(TestCase):
    
    def test_registration_get(self):
        response = self.client.get(reverse('registration'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/registration.html')
        self.assertIn('form', response.context)

    def test_registration_post_valid(self):
        valid_data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'email': 'testuser@example.com',
            'role': 'manager',  # <--- include role here
        }

        response = self.client.post(reverse('registration'), data=valid_data)

        # Check if it redirects after successful registration
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('loginpage'))

        # Confirm user is created
        user = get_user_model().objects.get(username='testuser')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertEqual(user.role, 'manager')  # <--- confirm role



class LoginViewTest(TestCase):

    def setUp(self):
       
        self.admin_user = get_user_model().objects.create_user(
            username='adminuser', password='adminpass', role='admin'
        )
        self.manager_user = get_user_model().objects.create_user(
            username='manageruser', password='managerpass', role='manager'
        )
        self.employee_user = get_user_model().objects.create_user(
            username='employeeuser', password='employeepass', role='employee'
        )

    def test_login_get(self):
        response = self.client.get(reverse('loginpage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertIn('form', response.context)

    def test_login_admin_user_redirect(self):
       
        response = self.client.post(reverse('loginpage'), {
        'username': 'adminuser',
        'password': 'adminpass'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('admin_dashboard'))

    def test_login_manager_user_redirect(self):
        response = self.client.post(reverse('loginpage'), {
        'username': 'manageruser',
        'password': 'managerpass'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('manager_dashboard'))

    def test_login_employee_user_redirect(self):
        response = self.client.post(reverse('loginpage'), {
            'username': 'employeeuser',
            'password': 'employeepass'
        })
        self.assertRedirects(response, reverse('employee_dashboard'))

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse('loginpage'), {
            'username': 'wronguser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, "Invalid credentials or user does not exist.")

    def test_login_empty_form(self):
        response = self.client.post(reverse('loginpage'), {
            'username': '',
            'password': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, "Please fill in both username and password.")


class LogoutViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword',
            role='employee'
        )

    def test_logout_redirects_to_login(self):
       
        self.client.login(username='testuser', password='testpassword')       
        response = self.client.get('/') 
        self.assertTrue('_auth_user_id' in self.client.session)        
        response = self.client.get(reverse('logout'))        
        self.assertNotIn('_auth_user_id', self.client.session)        
        self.assertRedirects(response, reverse('loginpage'))


def setUp(self):
    self.employee = get_user_model().objects.create_user(
        username='employeeuser', password='employeepass', role='employee'
    )
    self.client.login(username='employeeuser', password='employeepass')   
    self.completed_status = Statuses.objects.create(status_type='completed')
    self.pending_status = Statuses.objects.create(status_type='Not Started')   
    self.task1 = Task.objects.create(
        name='Task 1',
        employee=self.employee,
        status=self.completed_status,
        description='Test task 1'
    )
    self.task2 = Task.objects.create(
        name='Task 2',
        employee=self.employee,
        status=self.pending_status,
        description='Test task 2'
    )

    
    WorkLog.objects.create(user=self.employee, hours=3, date=date.today())
    WorkLog.objects.create(user=self.employee, hours=2, date=date.today())

    self.url = reverse('employee_dashboard')


def setUp(self):
    self.user = get_user_model().objects.create_user(
        username='testuser',
        password='testpass',
        role='employee'
    )
    self.client.login(username='testuser', password='testpass')   
    self.status = Statuses.objects.create(status_type='in_progress')   
    self.project = Project.objects.create(
        name='Project Alpha',
        description='A test project',
        created_by=self.user,
        assigned_to=self.user,
        start_date=date.today(),
        end_date=date.today(),
        status=self.status
    )

   
    self.task1 = Task.objects.create(
        name='Task 1',
        description='Task 1 description',
        employee=self.user,
        status=self.status,
        project=self.project,
        due_date=date.today()
    )

    self.task2 = Task.objects.create(
        name='Task 2',
        description='Task 2 description',
        employee=self.user,
        status=self.status,
        project=self.project,
        start_date=date.today(),
        due_date=date.today()
    )

    self.url = reverse('project_detail', args=[self.project.id])


def setUp(self):
    self.password = 'testpass'
    self.user = get_user_model().objects.create_user(
        username='testuser',
        password=self.password,
        role='employee'
    )

    self.other_user = get_user_model().objects.create_user(
        username='otheruser',
        password='otherpass',
        role='employee'
    )

  
    self.status_in_progress = Statuses.objects.create(status_type='in_progress')
    self.status_completed = Statuses.objects.create(status_type='completed')
    self.status_pending = Statuses.objects.create(status_type='pending')  # if needed

    self.project1 = Project.objects.create(
        name='Test Project',
        description='Test description',
        created_by=self.user,
        assigned_to=self.user,
        start_date=now().date(),
        end_date=now().date() + timedelta(days=10),
        status=self.status_in_progress
    )

    self.task1 = Task.objects.create(
        name='Task 1',
        description='Task 1 description',
        employee=self.user,
        project=self.project1,
        status=self.status_in_progress,
        due_date=now().date()
    )

    self.url = reverse('user_detail', args=[self.user.id])
    self.client.login(username=self.user.username, password=self.password)




class CreateTaskViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.password = 'pass123'
        self.manager = get_user_model().objects.create_user(
            username='manager',
            password=self.password,
            role='manager'
        )
        self.employee = get_user_model().objects.create_user(
            username='employee1',
            password='pass123',
            role='employee'
        )

   
        self.status_not_started = Statuses.objects.create(status_type='Not Started')
        self.status_completed = Statuses.objects.create(status_type='completed')

        self.project = Project.objects.create(
            name='Project Test',
            description='Description',
            created_by=self.manager,
            assigned_to=self.manager,
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=7),
            status=self.status_not_started
        )

        self.url = reverse('create_task', args=[self.project.id])

       
        self.client.login(username='manager', password=self.password)
        session = self.client.session
        session['user_id'] = self.manager.id
        session.save()

    def test_get_request_renders_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_create.html')

    def test_post_creates_task_successfully(self):
        data = {
            'name': 'Task 1',
            'description': 'Test task',
            'priority': 'high',
            'status': self.status_not_started.id,
            'assigned_to': self.employee.id,
            'project': self.project.id,
            'due_date': (timezone.now() + timedelta(days=3)).date().isoformat()
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertTrue(content['success'])
        self.assertEqual(Task.objects.count(), 1)

    def test_prevent_more_than_3_high_priority_tasks(self):       
        for i in range(3):
            Task.objects.create(
                name=f'Task {i}',
                description='High priority',
                priority='high',
                status=self.status_not_started,
                created_by=self.manager,
                employee=self.employee,
                project=self.project,
                due_date=timezone.now().date() + timedelta(days=i+1),
                created_at=timezone.now(),
                updated_at=timezone.now()
            )

        data = {
            'name': 'Extra High Task',
            'description': 'Test block',
            'priority': 'high',
            'status': self.status_not_started.id,
            'assigned_to': self.employee.id,
            'project': self.project.id,
            'due_date': (timezone.now() + timedelta(days=5)).date().isoformat()
        }

        response = self.client.post(self.url, data)
        content = json.loads(response.content)
        self.assertFalse(content['success'])
        self.assertIn('already has 3 high-priority tasks', content['message'])

    def test_redirects_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url, follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/loginpage/?next={self.url}')


class WorkLogViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.password = 'testpass123'
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password=self.password,
            role='employee'
        )
        self.status = Statuses.objects.create(status_type='In progress')
        self.completed_status = Statuses.objects.create(status_type='completed')  # 👈 This is key!

        self.project = Project.objects.create(
            name='Test Project',
            description='Test Description',
            created_by=self.user,
            assigned_to=self.user,
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=7),
            status=self.status
        )

        self.task = Task.objects.create(
            name='Test Task',
            description='Task desc',
            project=self.project,
            employee=self.user,
            status=self.status,
            due_date=timezone.now().date()
        )

        self.url = reverse('work_log')
        self.client.login(username='testuser', password=self.password)

    def test_get_request_renders_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'work_log_form.html')

    def test_successful_work_log_submission(self):
        data = {
            'hours': 4,
            'description': 'Worked on task',
            'task': self.task.id,
            'date': timezone.now().date().isoformat()
        }
        response = self.client.post(self.url, data, follow=True)

        messages = [msg.message for msg in get_messages(response.wsgi_request)]
        self.assertIn("Work log submitted successfully!", messages)
        self.assertEqual(WorkLog.objects.count(), 1)

    def test_prevent_logging_more_than_8_hours(self):       
        WorkLog.objects.create(
            user=self.user,
            task=self.task,
            hours=6,
            description='Initial log',
            date=timezone.now().date()
        )

        data = {
            'hours': 3, 
            'description': 'Extra hours',
            'task': self.task.id,
            'date': timezone.now().date().isoformat()
        }

        response = self.client.post(self.url, data, follow=True)

        messages = [msg.message for msg in get_messages(response.wsgi_request)]
        self.assertIn("You cannot log more than 8 hours in a day.", messages)
        self.assertEqual(WorkLog.objects.count(), 1)  

    def test_redirects_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url, follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/loginpage/?next={self.url}')



class DoTaskViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.password = 'testpass123'
        self.user = get_user_model().objects.create_user(
            username='employee1',
            password=self.password,
            role='employee'
        )

        self.status1 = Statuses.objects.create(status_type='In progress')
        self.status2 = Statuses.objects.create(status_type='completed')

        self.project = Project.objects.create(
            name='Project X',
            description='Test project',
            created_by=self.user,
            assigned_to=self.user,
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=7),
            status=self.status1
        )

        self.task = Task.objects.create(
            name='Test Task',
            description='Test desc',
            project=self.project,
            employee=self.user,
            status=self.status1,
            due_date=timezone.now().date()
        )

        self.url = reverse('do_task', args=[self.task.id])
        self.client.login(username='employee1', password=self.password)

    def test_get_request_renders_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'do_task.html')

    
    def test_post_rejects_large_file(self):
        big_file = SimpleUploadedFile(
            "large_file.txt",
            b"x" * 6 * 1024 * 1024,  # 6 MB
            content_type="text/plain"
        )
        data = {
            'statusid': self.status2.id,
            'uploadfile': big_file
        }
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'This file is more than 5KB', response.content)

    def test_post_accepts_valid_file(self):
        small_file = SimpleUploadedFile(
            "small_file.txt",
            b"hello world!",
            content_type="text/plain"
        )
        data = {
            'statusid': self.status2.id,
            'uploadfile': small_file
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'File has successfully been uploaded', response.content)

    def test_redirects_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url, follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/loginpage/?next={self.url}')


