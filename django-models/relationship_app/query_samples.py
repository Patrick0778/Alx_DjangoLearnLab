import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django-models.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
def get_books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    return author.books.all()

# List all books in a library
def get_books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.books.all()

# Retrieve the librarian for a library
def get_librarian_of_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.librarian

# Sample usage
if __name__ == "__main__":
    print("Books by author:", list(get_books_by_author("J.K. Rowling")))
    print("Books in library:", list(get_books_in_library("Central Library")))
    print("Librarian of library:", get_librarian_of_library("Central Library"))
