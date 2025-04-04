from django.http import HttpResponseForbidden

class RoleBasedAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the response from the next middleware/view
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            # Check if the view requires a specific role
            if hasattr(view_func, 'role_required'):
                required_role = view_func.role_required
                print(request.user.role)  # Debugging output
                
                # Check if the user's role matches the required role for the view
                if request.user.role != required_role:
                    # If not, return a forbidden response
                    return HttpResponseForbidden("You do not have permission to access this page.")
        
        return None
