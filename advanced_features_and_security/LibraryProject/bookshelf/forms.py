from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.html import escape
from .models import Book, CustomUser

class ExtendedUserCreationForm(UserCreationForm):
    """
    Enhanced user creation form with additional security validations.
    SECURITY: Implements strong password policies and email uniqueness checks.
    """
    email = forms.EmailField(required=True)
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email')

    def clean_password2(self):
        """
        SECURITY: Validates password strength to ensure secure passwords.
        Implements multiple checks:
        - Password match verification
        - Minimum length requirement (8 characters)
        - Requires at least one number
        - Requires at least one uppercase letter
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        
        # Password strength validation
        if len(password1) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in password1):
            raise ValidationError("Password must contain at least one number")
        if not any(char.isupper() for char in password1):
            raise ValidationError("Password must contain at least one uppercase letter")
        
        return password2

    def clean_email(self):
        """
        SECURITY: Ensures email uniqueness to prevent duplicate registrations 
        and potential account takeovers.
        """
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered")
        return email

    def save(self, commit=True):
        """
        SECURITY: Uses Django's secure password hashing mechanism through set_password().
        Sets default role to lowest privilege level (MEMBER) following principle of least privilege.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            user.profile.role = 'MEMBER'
            user.profile.save()
        return user

class BookForm(forms.ModelForm):
    """
    Form for book creation/editing with security validations.
    SECURITY: Implements input validation and sanitization to prevent XSS attacks.
    """
    def clean_title(self):
        """
        SECURITY: Sanitizes user input by:
        - Escaping HTML characters to prevent XSS attacks
        - Validating length requirements
        - Removing leading/trailing whitespace
        """
        title = self.cleaned_data.get('title')
        if title:
            title = escape(title.strip())
            if len(title) < 1 or len(title) > 200:
                raise ValidationError('Title must be between 1 and 200 characters.')
        return title

    class Meta:
        model = Book
        fields = ['title', 'author']

class ExampleForm(forms.Form):
    """
    Example form with security validations for demonstration purposes.
    SECURITY: Implements input validation and sanitization to prevent XSS attacks.
    """
    name = forms.CharField(
        max_length=100, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        max_length=1000
    )
    
    def clean_name(self):
        """
        SECURITY: Sanitizes user input by escaping HTML characters to prevent XSS attacks.
        """
        name = self.cleaned_data.get('name')
        if name:
            name = escape(name.strip())
            if len(name) < 2:
                raise ValidationError('Name must be at least 2 characters long.')
        return name
    
    def clean_message(self):
        """
        SECURITY: Sanitizes user input in the message field to prevent XSS attacks.
        """
        message = self.cleaned_data.get('message')
        if message:
            message = escape(message.strip())
        return message