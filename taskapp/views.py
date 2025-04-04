from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomUserRegistrationForm, LoginForm
from .models import CustomUser, Project, Task, Statuses, WorkLog, EmployeePerformanceReport
from django.utils import timezone
from django.db.models import Sum
from django.http import JsonResponse, HttpResponse
from datetime import time, datetime
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout as authlogout,login as authlogin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task, EmployeePerformanceReport, Statuses
from django.utils import timezone
from django.db.models import Count



def registration(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('loginpage')  
    else:
        form = CustomUserRegistrationForm()

    return render(request, 'registration/registration.html', {'form': form})


def loginpage(request):
    error_message = None
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                request.session['user_id'] = user.id
                print(request.session['user_id'])
                authlogin(request, user)

               
                if user.role == 'admin':
                    return redirect('admin_dashboard')
                elif user.role == "employee":
                    return redirect('employee_dashboard')
                else:
                    return redirect('manager_dashboard')
            else:
                error_message = "Invalid credentials or user does not exist."
        else:
            error_message = "Please fill in both username and password."

    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form, 'error_message': error_message})


def role_required(role):
    def decorator(view_func):
        view_func.role_required = role
        return view_func
    return decorator

@login_required
@role_required('admin')
def admin_dashboard(request):
    if not request.user.role == 'admin':
        return redirect('home')
    
    users = CustomUser.objects.all()
    projects = Project.objects.all()
    return render(request, 'admin_dashboard.html', {'users': users, 'projects': projects})

    
@login_required
@role_required('manager')
def manager_dashboard(request):
    if not request.user.role == 'manager':
        return redirect('home')
    project = Project.objects.filter(assigned_to=request.user)
    
    return render(request, 'manager_dashboard.html', {'project': project})


@login_required
@role_required('employee')
def employee_dashboard(request):
    tasks = Task.objects.filter(employee=request.user)
    completed_task_count = tasks.filter(status=2).count()
    total_task_count = tasks.count()
    total_hours = WorkLog.objects.filter(user =request.user).aggregate(Sum('hours'))['hours__sum']
    total_hours_worked = total_hours if total_hours else 0

    print(total_hours_worked)
    return render(request, 'employee_dashboard.html', {
        'tasks': tasks,
        'completed_task_count': completed_task_count,
        'total_task_count': total_task_count,
        'total_hours_worked': total_hours_worked
    })


@login_required
@role_required('manager')
def create_task(request, id):
    print(id)
    print(id)
    print(id)
    project = get_object_or_404(Project, id=id)
    users = CustomUser.objects.filter(role="employee")  
    status_details = Statuses.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        status_name = request.POST.get('status')
        print(status_name)
        assigned_to = request.POST.get('assigned_to') 
        project_id = request.POST.get('project')  
        due_date = request.POST.get('due_date')
        created = request.session.get('user_id')  
        created_by = CustomUser.objects.get(id=created)

        try:
            
            assigned_user = CustomUser.objects.get(id=assigned_to)
            project = Project.objects.get(id=project_id)
            status = Statuses.objects.get(id=status_name)  
            
            high_priority_tasks = Task.objects.filter(
                employee=assigned_user, 
                priority="high", 
                
            ).count()
            
            if high_priority_tasks >= 3 and priority == "high":
                return JsonResponse({'success': False, 'message': 'This employee already has 3 high-priority tasks. Cannot assign more.'})
                
        except (CustomUser.DoesNotExist, Project.DoesNotExist):
            return JsonResponse({'success': False, 'message': 'User or Project not found.'})

       
        new_task = Task(
            name=name,
            description=description,
            priority=priority,
            status=status,
            created_by=created_by,
            employee=assigned_user,
            project=project,  
            due_date=due_date,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )
        new_task.save()

        
        return JsonResponse({'success': True, 'message': 'Task created successfully!'})

    return render(request, 'task_create.html', {
        'project': project,
        'status_details': status_details,  
    })





@login_required
def work_log_view(request):
    print(request.user)
    
    date_str = request.POST.get('date', '').strip()

    if date_str:
        try:
           
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            
            date = datetime.today().date()
    else:
        
        date = datetime.today().date()
    
    
    total_hours_worked = WorkLog.objects.filter(user=request.user,date=date).aggregate(Sum('hours'))['hours__sum'] or 0
    print(total_hours_worked)
    
    
    if request.method == "POST":
        hours_worked = float(request.POST['hours'])
        print(hours_worked)
        task = request.POST.get('task')
        print(task)
        print
        
        
        if total_hours_worked + hours_worked > 8:
            
            return render(request, 'work_log_form.html', {'task': task, 'total_hours_worked': total_hours_worked, 'error_message': "You cannot log more than 8 hours in a day."})
        
        # Log the work hours
        description = request.POST['description']
        task_instance = Task.objects.get(id=task)
        WorkLog.objects.create(
            task=task_instance,
            user=request.user,
            hours=hours_worked,
            description=description,
            date=date  
        )
        return redirect('employee_dashboard')  
    
    return render(request, 'work_log_form.html', {'task': task, 'total_hours_worked': total_hours_worked, 'date': date})


def project_detail(request, project_id):
    project = Project.objects.get(id=project_id)
    tasks = Task.objects.filter(project=project)
    return render(request, 'project_detail.html', {'project': project, 'tasks': tasks})




def home(request):
    return render(request, 'home.html')


@login_required
@role_required('admin')
def user_detail(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'user_detail.html', {'user': user})




def logout(request):
    authlogout(request)
    return redirect('loginpage')



@login_required
@role_required('admin')
def create_project(request):
    managers = CustomUser.objects.filter(role="manager")
    status_details = Statuses.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        admin_id = request.session.get('user_id')  
        print(admin_id)
        manager_id = request.POST.get('manager')  
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        status = request.POST.get('status')
   
        try:
            created_by = CustomUser.objects.get(id=admin_id)
            manager_instance = CustomUser.objects.get(id=manager_id)
        except CustomUser.DoesNotExist:
            messages.error(request, "Manager not found.")
            return redirect('create_project') 
  
        new_project = Project(
            name=name,
            description=description,
            created_by=created_by,
            assigned_to = manager_instance,
            start_date=start_date,
            end_date=end_date,
            status=status,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )

        new_project.save()
        messages.success(request, "Project created successfully!")
        return redirect('project_list')  
    return render(request, 'create_project.html', {'managers': managers})

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project_list.html', {'projects': projects})

def task_list(request):
    user=request.session.get('user_id')
    print (user)
    tasks = Task.objects.select_related('employee').filter(created_by=user)

    return render(request, 'task_list.html', {'tasks': tasks})


def calculate_total_work_hours(user):
    total_hours = WorkLog.objects.filter(user=user).aggregate(Sum('hours_worked'))['hours_worked__sum']
    return total_hours if total_hours else 0  

@login_required
@role_required('employee')
def do_task(request, id):
    task_details = get_object_or_404(Task, id=id) 
    status = Statuses.objects.all()


    if request.method == 'POST':
        status_id = request.POST.get('statusid')
        print(status_id)
        uploadfile = request.FILES.get('uploadfile', None)
        print(f"Uploaded file: {uploadfile}")
        
        
        if uploadfile and uploadfile.size > 5242880: 
           

            return HttpResponse("This file is more than 5KB", status=400)
        else:

            return HttpResponse("File has successfully been uploaded")

        if status_id:
            task_details.status = Status.objects.get(id=status_id)
            task_details.file = uploadfile

            task.save()
            return redirect('assigntaskview')
            messages.success(request, "Task status updated successfully.")
            

    return render(request, 'do_task.html', {
        'task_details': task_details,
        'status': status
    })


@login_required
@role_required('admin')
def statustype(request):
    if request.method == "POST":
        statustype=request.POST.get('statustype')
        print(statustype)
        status_reg=Statuses()
        status_reg.status_type=statustype
        status_reg.save()


    return render(request,'status.html') 


def update_staus(request):
    if request.method == "POST":
        id = request.POST.get('id') 
        print(id)

        
        status_id = request.POST.get('statusid')
        print(status_id)

        uploadfile = request.FILES.get('uploadfile')
        print(uploadfile)

        tasks = get_object_or_404(Task, id=id)
        
        
        tasks.status_id = status_id 
        tasks.file = uploadfile  
        
        
        tasks.save() 
        
       
        return JsonResponse({"success": True, "message": "Status updated successfully!"})

    
    return JsonResponse({"success": False, "message": "Invalid request method."})


@receiver(post_save, sender=Task)
def generate_performance_report(sender, instance, created, **kwargs):
    if created:  
        employee = instance.employee  
        completed_status = Statuses.objects.get(status_type='completed') 
        if instance.status == completed_status: 
           
            completed_tasks_count = Task.objects.filter(
                employee=employee, 
                status=completed_status
            ).count()
            
            print(f"Completed tasks count for {employee.username}: {completed_tasks_count}")
            
            if completed_tasks_count == 5:  
                EmployeePerformanceReport.objects.create(
                    employee=employee,
                    report_date=timezone.now()
                )
                print(f"Performance report created for {employee.username}")
            else:
                print(f"Performance report not created for {employee.username} as the count is {completed_tasks_count}")












