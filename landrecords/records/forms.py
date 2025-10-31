from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import LandRecord, UserProfile

class UserRegisterForm(UserCreationForm):
    """Form for user registration with additional fields"""
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    """Form for updating user information"""
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    """Form for updating user profile information"""
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address']

class LandRecordForm(forms.ModelForm):
    """Form for creating and updating land records"""
    class Meta:
        model = LandRecord
        fields = [
            'title', 'property_address', 'description', 'category',
            'document', 'survey_number', 'property_size', 'property_type'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'property_address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super(LandRecordForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'document':
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs.update({'class': 'form-control-file'})
    
    def clean_document(self):
        document = self.cleaned_data.get('document', False)
        if document:
            # Validate file size (max 10MB)
            if document.size > 10 * 1024 * 1024:
                raise forms.ValidationError("File size must be under 10MB")
            
            # Validate file extension
            valid_extensions = ['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png']
            file_ext = document.name.split('.')[-1].lower()
            if file_ext not in valid_extensions:
                raise forms.ValidationError(
                    f"Unsupported file type. Allowed types: {', '.join(valid_extensions)}"
                )
        return document
