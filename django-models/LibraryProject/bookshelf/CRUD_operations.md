# CRUD Operations Summary

## Create

> > > from bookshelf.models import Book
> > > book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
> > > book

# Output: <Book: 1984>

## Retrieve

> > > book = Book.objects.get(title="1984")
> > > book.title, book.author, book.publication_year

# Output: ("1984", "George Orwell", 1949)

## Update

> > > book = Book.objects.get(title="1984")
> > > book.title = "Nineteen Eighty-Four"
> > > book.save()
> > > book.title

# Output: "Nineteen Eighty-Four"

## Delete

> > > book = Book.objects.get(title="Nineteen Eighty-Four")
> > > book.delete()
> > > list(Book.objects.all())

# Output: []
