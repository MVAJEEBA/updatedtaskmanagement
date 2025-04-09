from django import forms
# from .models import Project
from django import forms
from .models import Task
# # forms.py

# from django import forms
from .models import WorkLog  # Import WorkLog model


from django import forms
# from .models import Project
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from django import forms
from .models import Task



class TaskAssignmentForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'priority', 'employee']
    
    def clean(self):
        employee = self.cleaned_data['employee']
        high_priority_tasks = Task.objects.filter(employee=employee, priority='high')
        
        if high_priority_tasks.count() >= 3:
            raise forms.ValidationError("Employee cannot have more than 3 high-priority tasks.")
        
        return self.cleaned_data

class WorkLogForm(forms.ModelForm):
    class Meta:
        model = WorkLog
        fields = ['date', 'hours', 'description']
    
    def clean(self):
        hours = self.cleaned_data['hours']
        if hours > 8:
            raise forms.ValidationError("Cannot log more than 8 hours in a single day.")
        
        description = self.cleaned_data['description']
        if len(description) < 20:
            raise forms.ValidationError("Description must be at least 20 characters long.")
        
        return self.cleaned_data



from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re
from .models import CustomUser

class CustomUserRegistrationForm(UserCreationForm):
    # Add additional fields for role
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES, 
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].label = "User Role"
        self.fields['role'].help_text = "Select the role for the user (admin, manager, employee)"
        
        # Label and help text customization for other fields
        self.fields['username'].label = "Username"
        self.fields['email'].label = "Email"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Ensure the username only contains letters (no numbers or special characters)
        if not re.match('^[A-Za-z]+$', username):
            raise ValidationError("Username must only contain letters (no digits or symbols).")
        return username




class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))




class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status']






