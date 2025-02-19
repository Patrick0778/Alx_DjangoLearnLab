from django.contrib import admin
from .models import Book

admin.site.register(Book)

class BookAdmin(admin.ModelAdmin):
    # Define the columns to display in the list view
    list_display = ('title', 'author', 'publication_year')

    # Add search capability for title and author fields
    search_fields = ('title', 'author')

    # Add list filters for publication year
    list_filter = ('publication_year',)
