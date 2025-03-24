from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from relationship_app.models import Book

def is_member(user):
    return user.is_authenticated and user.profile.role == 'MEMBER'

@user_passes_test(is_member)
def member_view(request):
    books = Book.objects.select_related('author').all()
    context = {
        'books': books,
        'title': 'Available Books',
        'role': 'Member'
    }
    return render(request, 'relationship_app/role_views/member_view.html', context)