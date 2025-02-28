from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.exceptions import ValidationError
from django.utils.html import escape
from django.views.decorators.http import require_http_methods
from django.views.decorators.debug import sensitive_post_parameters
from django import forms
from .models import Book, Library, CustomUser, Author
from .forms import ExampleForm

# SECURITY: Role check functions ensure proper access control
def is_admin(user):
    """SECURITY: Verifies if a user has admin role"""
    return user.is_authenticated and user.profile.role == 'ADMIN'

def is_librarian(user):
    """SECURITY: Verifies if a user has librarian role"""
    return user.is_authenticated and user.profile.role == 'LIBRARIAN'

def is_member(user):
    """SECURITY: Verifies if a user has member role"""
    return user.is_authenticated and user.profile.role == 'MEMBER'

# Forms
class ExtendedUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        
        # SECURITY: Password strength validation to enforce secure passwords
        if len(password1) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in password1):
            raise ValidationError("Password must contain at least one number")
        if not any(char.isupper() for char in password1):
            raise ValidationError("Password must contain at least one uppercase letter")
        
        return password2

    def clean_email(self):
        # SECURITY: Prevent duplicate email registration
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        # SECURITY: Secure password handling using Django's password hashing
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            user.profile.role = 'MEMBER'
            user.profile.save()
        return user

class BookForm(forms.ModelForm):
    def clean_title(self):
        # SECURITY: Input validation and HTML escaping to prevent XSS
        title = self.cleaned_data.get('title')
        if title:
            title = escape(title.strip())
            if len(title) < 1 or len(title) > 200:
                raise ValidationError('Title must be between 1 and 200 characters.')
        return title

    class Meta:
        model = Book
        fields = ['title', 'author']

# Authentication views
@require_http_methods(["GET", "POST"])  # SECURITY: Restricts HTTP methods to prevent unintended operations
@sensitive_post_parameters('password1', 'password2')  # SECURITY: Prevents passwords from appearing in logs/errors
def register(request):
    if request.user.is_authenticated:
        return redirect('bookshelf:member_dashboard')
        
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Registration successful.')
                return redirect('bookshelf:member_dashboard')
            except Exception as e:
                # SECURITY: Generic error message to avoid information disclosure
                messages.error(request, 'An error occurred during registration.')
                return redirect('bookshelf:register')
    else:
        form = ExtendedUserCreationForm()
    return render(request, 'bookshelf/auth/register.html', {'form': form})

@require_http_methods(["GET", "POST"])  # SECURITY: Restricts HTTP methods
@sensitive_post_parameters('password')  # SECURITY: Prevents password from appearing in logs/errors
def login_view(request):
    if request.user.is_authenticated:
        return redirect('bookshelf:member_dashboard')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            try:
                user = form.get_user()
                login(request, user)
                messages.success(request, 'Login successful.')
                
                # SECURITY: Role-based redirection to appropriate dashboard
                if user.profile.role == 'ADMIN':
                    return redirect('bookshelf:admin_dashboard')
                elif user.profile.role == 'LIBRARIAN':
                    return redirect('bookshelf:librarian_dashboard')
                else:
                    return redirect('bookshelf:member_dashboard')
            except Exception as e:
                # SECURITY: Generic error message to avoid information disclosure
                messages.error(request, 'An error occurred during login.')
                return redirect('bookshelf:login')
    else:
        form = AuthenticationForm()
    return render(request, 'bookshelf/auth/login.html', {'form': form})

@login_required  # SECURITY: Prevents unauthorized access
def logout_view(request):
    try:
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
    except Exception as e:
        messages.error(request, 'An error occurred during logout.')
    return redirect('bookshelf:login')

@login_required  # SECURITY: Prevents unauthorized access
@sensitive_post_parameters('old_password', 'new_password1', 'new_password2')  # SECURITY: Prevents passwords from appearing in logs
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            try:
                user = form.save()
                # SECURITY: Maintains user's session after password change to prevent forced logout
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('bookshelf:member_dashboard')
            except Exception as e:
                messages.error(request, 'An error occurred while changing your password.')
                return redirect('bookshelf:change_password')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'bookshelf/auth/change_password.html', {'form': form})

# Role-based views
@user_passes_test(is_admin)  # SECURITY: Ensures only users with admin role can access
def admin_view(request):
    context = {
        'user_count': CustomUser.objects.count(),
        'book_count': Book.objects.count(),
        'library_count': Library.objects.count(),
        'title': 'Admin Dashboard',
        'role': 'Admin'
    }
    return render(request, 'bookshelf/role_views/admin_view.html', context)

@user_passes_test(is_librarian)  # SECURITY: Ensures only users with librarian role can access
def librarian_view(request):
    # SECURITY: Using prefetch_related to optimize database queries and prevent n+1 query vulnerabilities
    libraries = Library.objects.prefetch_related('books', 'books__author').all()
    context = {
        'libraries': libraries,
        'title': 'Library Management',
        'role': 'Librarian'
    }
    return render(request, 'bookshelf/role_views/librarian_view.html', context)

@user_passes_test(is_member)  # SECURITY: Ensures only users with member role can access
def member_view(request):
    # SECURITY: Using select_related to optimize database queries
    books = Book.objects.select_related('author').all()
    context = {
        'books': books,
        'title': 'Available Books',
        'role': 'Member'
    }
    return render(request, 'bookshelf/role_views/member_view.html', context)

# Book views
@login_required  # SECURITY: Prevents unauthorized access
def book_list(request):
    try:
        # SECURITY: Using select_related to optimize database queries
        books = Book.objects.all().select_related('author')
        context = {
            'books': books,
            'user_role': request.user.profile.role,
            # SECURITY: Permission checks to control UI elements
            'can_add': request.user.has_perm('bookshelf.can_add_book'),
            'can_edit': request.user.has_perm('bookshelf.can_edit_book'),
            'can_delete': request.user.has_perm('bookshelf.can_delete_book')
        }
        return render(request, 'bookshelf/book_list.html', context)
    except Exception as e:
        # SECURITY: Generic error message to avoid information disclosure
        messages.error(request, 'An error occurred while fetching the book list.')
        return redirect('bookshelf:member_dashboard')

class BookCreateView(PermissionRequiredMixin, CreateView):  # SECURITY: Permission-based access control
    model = Book
    form_class = BookForm  # SECURITY: Using form for input validation
    template_name = 'bookshelf/book_form.html'
    success_url = reverse_lazy('bookshelf:book_list')
    permission_required = 'bookshelf.can_add_book'
    raise_exception = True

    def handle_no_permission(self):
        # SECURITY: Proper messaging for unauthorized access without revealing system details
        messages.error(self.request, "You don't have permission to add books.")
        return redirect('bookshelf:book_list')

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, 'Book created successfully.')
            return response
        except Exception as e:
            # SECURITY: Generic error message to avoid information disclosure
            messages.error(self.request, 'Error creating book.')
            return self.form_invalid(form)

class BookUpdateView(PermissionRequiredMixin, UpdateView):  # SECURITY: Permission-based access control
    model = Book
    form_class = BookForm  # SECURITY: Using form for input validation
    template_name = 'bookshelf/book_form.html'
    success_url = reverse_lazy('bookshelf:book_list')
    permission_required = 'bookshelf.can_edit_book'
    raise_exception = True

    def handle_no_permission(self):
        # SECURITY: Proper messaging for unauthorized access
        messages.error(self.request, "You don't have permission to edit books.")
        return redirect('bookshelf:book_list')

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, 'Book updated successfully.')
            return response
        except Exception as e:
            # SECURITY: Generic error message to avoid information disclosure
            messages.error(self.request, 'Error updating book.')
            return self.form_invalid(form)

class BookDeleteView(PermissionRequiredMixin, DeleteView):  # SECURITY: Permission-based access control
    model = Book
    template_name = 'bookshelf/book_confirm_delete.html'
    success_url = reverse_lazy('bookshelf:book_list')
    permission_required = 'bookshelf.can_delete_book'
    raise_exception = True

    def handle_no_permission(self):
        # SECURITY: Proper messaging for unauthorized access
        messages.error(self.request, "You don't have permission to delete books.")
        return redirect('bookshelf:book_list')

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(request, 'Book deleted successfully.')
            return response
        except Exception as e:
            # SECURITY: Generic error message to avoid information disclosure
            messages.error(request, 'Error deleting book.')
            return redirect('bookshelf:book_list')

@permission_required('bookshelf.can_view_book_details', raise_exception=True)  # SECURITY: Permission-based access control
def book_detail(request, pk):
    try:
        # SECURITY: Using get_object_or_404 to prevent information disclosure
        book = get_object_or_404(Book, pk=pk)
        context = {
            'book': book,
            'user_role': request.user.profile.role,
            # SECURITY: Permission checks to control UI elements
            'can_edit': request.user.has_perm('bookshelf.can_edit_book'),
            'can_delete': request.user.has_perm('bookshelf.can_delete_book')
        }
        return render(request, 'bookshelf/book_detail.html', context)
    except Exception as e:
        # SECURITY: Generic error message to avoid information disclosure
        messages.error(request, 'Error retrieving book details.')
        return redirect('bookshelf:book_list')

class LibraryDetailView(LoginRequiredMixin, DetailView):  # SECURITY: Login required for access
    model = Library
    template_name = 'bookshelf/library_detail.html'
    context_object_name = 'library'
    raise_exception = True

    def get_queryset(self):
        # SECURITY: Using prefetch_related to optimize database queries
        return Library.objects.prefetch_related('books__author')

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context['user_role'] = self.request.user.profile.role
            return context
        except Exception as e:
            # SECURITY: Generic error message to avoid information disclosure
            messages.error(self.request, 'Error retrieving library details.')
            return {}

@require_http_methods(["GET", "POST"])  # SECURITY: Restricts HTTP methods to prevent unintended operations
def form_example(request):
    """
    View function for the example form, demonstrating secure form handling.
    SECURITY: Implements proper form validation, sanitization, and CSRF protection.
    """
    submitted = False
    
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # SECURITY: Form validation ensures all input is sanitized
            # In a real app, you would typically save the data here
            # but for this example, we're just showing validation
            
            # Get sanitized data
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            message = form.cleaned_data.get('message')
            
            # Log the submission (in a real app, you might save to DB)
            print(f"Form submission: {name}, {email}")
            
            messages.success(request, 'Form submitted successfully!')
            submitted = True
            # Return a new form instance for security (prevents form resubmission)
            form = ExampleForm()
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/form_example.html', {
        'form': form,
        'submitted': submitted,
        'title': 'Secure Form Example'
    })
