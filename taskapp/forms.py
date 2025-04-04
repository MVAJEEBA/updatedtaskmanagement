from django import forms
from .models import Project
from django import forms
from .models import Task
# # forms.py

# from django import forms
from .models import WorkLog  # Import WorkLog model


from django import forms
from .models import Project
from django.core.exceptions import ValidationError



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
from .models import CustomUser

class CustomUserRegistrationForm(UserCreationForm):
    # Add additional fields for role, first_name, last_name, etc.
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
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize field attributes or labels if needed
        self.fields['role'].label = "User Role"
        self.fields['role'].help_text = "Select the role for the user (admin, manager, employee)"


from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status']







