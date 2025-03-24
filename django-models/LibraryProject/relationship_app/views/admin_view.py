from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from relationship_app.models import Book, Library

def is_admin(user):
    return user.is_authenticated and user.profile.role == 'ADMIN'

@user_passes_test(is_admin)
def admin_view(request):
    context = {
        'user_count': User.objects.count(),
        'book_count': Book.objects.count(),
        'library_count': Library.objects.count(),
        'title': 'Admin Dashboard',
        'role': 'Admin'
    }
    return render(request, 'relationship_app/role_views/admin_view.html', context)