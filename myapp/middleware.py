from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve

class RoleBasedAccessControlMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_superuser:
            
            path_role_map = {
                '/index/': 'admin', 
                '/registration/': 'admin',
                '/employeesregistration/': 'admin',
                '/taskcategory/': 'admin',
                '/statustype/': 'admin',
                'employees/userindex/': 'user',
                'employees/assigntaskview/': 'user',
                '/manager/managerindex/': 'manager',
                '/manager/manageremployeesview/': 'manager',
                'manager/taskassignview': 'manager',
            }
            
            role_priority = ['admin', 'manager', 'user']
            
            if request.path in path_role_map:
                required_role = path_role_map[request.path]
                
                # Check if the user has the required role
                if not request.user.groups.filter(name=required_role).exists():
                    role=request.user.role
                    if request.user.role == 'admin':
                        return redirect('index')
                        
                    elif request.user.role == 'user':
                        return redirect('userindex')
                    elif request.user.role == 'manager':
                        return redirect('managerindex')
                    else:
                        return redirect('loginpage')

        # Return the response if no redirects are triggered
        response = self.get_response(request)
        return response
