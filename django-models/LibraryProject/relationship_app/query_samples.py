from relationship_app.models import Author, Book, Library, Librarian

def query_books_by_author(author_name):
    # Query all books by a specific author
    try:
        author = Author.objects.get(name=author_name)
        return Book.objects.filter(author=author)
    except Author.DoesNotExist:
        return None

def list_library_books():
    # List all books in a library using the books relationship
    try:
        library = Library.objects.first()  # Get the first library
        return library.books.all()  # Use the books relationship to get all books
    except Library.DoesNotExist:
        return None

def get_library_librarian(library_name):
    # Retrieve the librarian for a library
    try:
        library = Library.objects.get(name=library_name)
        return Librarian.objects.get(library=library)
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None
