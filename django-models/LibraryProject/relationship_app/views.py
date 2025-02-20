from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import user_passes_test, permission_required
from .models import Book, Library, UserProfile
from .forms import BookForm  # Ensure you create this form in forms.py
from django.contrib.auth.models import Permission

# ===============================
# Book Management Views with Permissions
# ===============================

@permission_required('relationship_app.add_book', raise_exception=True)
def add_book(request):
    """
    View to allow authorized users to add a book.
    """
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm()
    return render(request, 'relationship_app/add_book.html', {'form': form})

@permission_required('relationship_app.change_book', raise_exception=True)
def edit_book(request, book_id):
    """
    View to allow authorized users to edit a book.
    """
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/edit_book.html', {'form': form, 'book': book})

@permission_required('relationship_app.delete_book', raise_exception=True)
def delete_book(request, book_id):
    """
    View to allow authorized users to delete a book.
    """
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        book.delete()
        return redirect('list_books')
    return render(request, 'relationship_app/delete_book.html', {'book': book})
