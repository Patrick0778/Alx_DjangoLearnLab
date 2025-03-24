from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import permission_required, login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import Library, Book

# Role check functions
def is_admin(user):
    return user.is_authenticated and user.profile.role == 'ADMIN'

def is_librarian(user):
    return user.is_authenticated and user.profile.role == 'LIBRARIAN'

def is_member(user):
    return user.is_authenticated and user.profile.role == 'MEMBER'

# Registration view and form
class ExtendedUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user.profile.role = 'MEMBER'  # Default role for new users
            user.profile.save()
        return user

def register(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('relationship_app:member_dashboard')
    else:
        form = ExtendedUserCreationForm()
    return render(request, 'relationship_app/auth/register.html', {'form': form})

# Role-based views
@user_passes_test(is_admin)
def Admin(request):
    context = {
        'user_count': User.objects.count(),
        'book_count': Book.objects.count(),
        'library_count': Library.objects.count(),
        'title': 'Admin Dashboard',
        'role': 'Admin'
    }
    return render(request, 'relationship_app/role_views/admin_view.html', context)

@user_passes_test(is_librarian)
def librarian_view(request):
    libraries = Library.objects.prefetch_related('books', 'books__author').all()
    context = {
        'libraries': libraries,
        'title': 'Library Management',
        'role': 'Librarian'
    }
    return render(request, 'relationship_app/role_views/librarian_view.html', context)

@user_passes_test(is_member)
def member_view(request):
    books = Book.objects.select_related('author').all()
    context = {
        'books': books,
        'title': 'Available Books',
        'role': 'Member'
    }
    return render(request, 'relationship_app/role_views/member_view.html', context)

# Book and Library views
class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'relationship_app/list_books.html'
    context_object_name = 'books'

    def get_queryset(self):
        return Book.objects.all().select_related('author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = self.request.user.profile.role
        return context

class LibraryDetailView(LoginRequiredMixin, DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_queryset(self):
        return Library.objects.prefetch_related('books__author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = self.request.user.profile.role
        return context
