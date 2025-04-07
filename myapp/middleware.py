from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve

class RoleBasedAccessControlMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_superuser:
            # Define a mapping of URL paths to roles
            path_role_map = {
                '/admin_dashboard/': 'admin', 
                 '/create_project/': 'admin', 
                'employee_dashboard/': 'employee',
                '/manager_dashboard/': 'manager',
                '/create_task/': 'manager',

            }
            
            # Role priority: Higher roles can access lower ones
            role_priority = ['admin', 'manager', 'employee']
            
            if request.path in path_role_map:
                required_role = path_role_map[request.path]

                # Check if the user has the required role or a higher role (based on priority)
                user_roles = [group.name for group in request.user.groups.all()]
                
                # Check if the user has the required role or any higher role in the priority list
                for role in role_priority:
                    if role in user_roles and role_priority.index(role) <= role_priority.index(required_role):
                        break
                else:
                    # No matching role found in the correct priority
                    if 'admin' in user_roles:
                        return redirect('admin_dashboard')
                    elif 'manager' in user_roles:
                        return redirect('manager_dashboard')
                    elif 'employee' in user_roles:
                        return redirect('employee_dashboard')
                    else:
                        return redirect('loginpage')

        # Return the response if no redirects are triggered
        response = self.get_response(request)
        return response
