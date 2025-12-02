"""
Form definitions for the attendance system
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Company, AttendanceRecord


class LoginForm(AuthenticationForm):
    """Custom login form"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )


class AttendanceRecordForm(forms.ModelForm):
    """Form for creating/editing attendance records"""
    class Meta:
        model = AttendanceRecord
        fields = [
            'ep_no', 'ep_name', 'company', 'date', 'shift', 'overstay', 'status',
            'in_time', 'out_time', 'in_time_2', 'out_time_2', 'in_time_3', 'out_time_3',
            'overtime', 'overtime_to_mandays'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': True}),
            'ep_no': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'ep_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'company': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'shift': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'overstay': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'status': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'in_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'out_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'in_time_2': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'out_time_2': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'in_time_3': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'out_time_3': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'overtime': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'overtime_to_mandays': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }
    
    def clean_date(self):
        """Validate that date is not in the future"""
        from datetime import date
        date_value = self.cleaned_data.get('date')
        if date_value and date_value > date.today():
            raise forms.ValidationError('Date cannot be in the future.')
        return date_value
    
    def clean_ep_no(self):
        """Validate employee number"""
        ep_no = self.cleaned_data.get('ep_no')
        if ep_no:
            ep_no = ep_no.strip()
            if not ep_no:
                raise forms.ValidationError('Employee number cannot be empty.')
        return ep_no
    
    def clean_ep_name(self):
        """Validate employee name"""
        ep_name = self.cleaned_data.get('ep_name')
        if ep_name:
            ep_name = ep_name.strip()
            if not ep_name:
                raise forms.ValidationError('Employee name cannot be empty.')
        return ep_name


class UserForm(forms.ModelForm):
    """Form for creating/editing users"""
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        help_text='Leave blank to keep current password (required for new users)',
        min_length=6
    )
    
    class Meta:
        model = User
        fields = ['username', 'role', 'company', 'assigned_date_from', 'assigned_date_to', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'role': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'company': forms.Select(attrs={'class': 'form-control'}),
            'assigned_date_from': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'assigned_date_to': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user', None)
        super().__init__(*args, **kwargs)
        
        # If admin user, restrict role choices to user1 only
        if self.request_user and self.request_user.role == 'admin':
            self.fields['role'].choices = [('user1', 'User1')]
            self.fields['company'].initial = self.request_user.company
            self.fields['company'].widget = forms.HiddenInput()
    
    def clean_username(self):
        """Validate username uniqueness"""
        username = self.cleaned_data.get('username')
        if username:
            username = username.strip().lower()
            # Check if username exists (excluding current instance)
            qs = User.objects.filter(username=username)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('This username is already taken.')
        return username
    
    def clean_password(self):
        """Validate password strength"""
        password = self.cleaned_data.get('password')
        
        # Password is required for new users
        if not self.instance.pk and not password:
            raise forms.ValidationError('Password is required for new users.')
        
        if password and len(password) < 6:
            raise forms.ValidationError('Password must be at least 6 characters long.')
        return password
    
    def clean(self):
        """Validate that admin and user1 roles have a company"""
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        company = cleaned_data.get('company')
        
        if role in ['admin', 'user1'] and not company:
            raise forms.ValidationError('Admin and User1 roles must have a company assigned.')
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        
        if password:
            user.set_password(password)
        
        if commit:
            user.save()
        
        return user
