from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import ViolationRecord, SSIOMember, Student, Violation, Reason

class LoginForm(forms.Form):
    """Form for user login"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username or Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

class ViolationRecordForm(forms.ModelForm):
    """Form for creating/editing violation records"""
    class Meta:
        model = ViolationRecord
        fields = ['violation', 'reason', 'description', 'photo_proof']
        widgets = {
            'violation': forms.Select(attrs={'class': 'form-control'}),
            'reason': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'photo_proof': forms.FileInput(attrs={'class': 'form-control'})
        }

class StudentForm(forms.ModelForm):
    """Form for student information"""
    class Meta:
        model = Student
        fields = ['name', 'student_id']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Student Full Name'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Student ID Number'})
        }

class SSIOMemberForm(forms.ModelForm):
    """Form for creating SSIO members"""
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators=[validate_password]
    )
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = SSIOMember
        fields = ['employee_id', 'role']
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'})
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match')
        
        return cleaned_data
    
    def save(self, commit=True):
        # Create a new User object
        user_data = {
            'username': self.cleaned_data['username'],
            'first_name': self.cleaned_data['first_name'],
            'last_name': self.cleaned_data['last_name'],
            'email': self.cleaned_data['email']
        }
        
        user = User(**user_data)
        user.set_password(self.cleaned_data['password'])
        user.save()
        
        # Create the SSIOMember object
        ssio_member = super().save(commit=False)
        ssio_member.user = user
        
        if commit:
            ssio_member.save()
        
        return ssio_member
