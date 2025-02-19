from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library

def list_books(request):
    """
    Function-based view to list all books.
    """
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})
class LibraryDetailView(DetailView):
    """
    Class-based view to display details of a specific library.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'