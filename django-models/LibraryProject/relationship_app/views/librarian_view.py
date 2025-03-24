from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from relationship_app.models import Library, Book

def is_librarian(user):
    return user.is_authenticated and user.profile.role == 'LIBRARIAN'

@user_passes_test(is_librarian)
def librarian_view(request):
    libraries = Library.objects.prefetch_related('books', 'books__author').all()
    context = {
        'libraries': libraries,
        'title': 'Library Management',
        'role': 'Librarian'
    }
    return render(request, 'relationship_app/role_views/librarian_view.html', context)