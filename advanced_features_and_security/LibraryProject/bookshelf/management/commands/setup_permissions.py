from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book

class Command(BaseCommand):
    help = 'Create default groups and permissions'

    def handle(self, *args, **options):
        # Create groups if they don't exist
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        librarian_group, _ = Group.objects.get_or_create(name='Librarian')
        member_group, _ = Group.objects.get_or_create(name='Member')

        # Get content type for Book model
        book_content_type = ContentType.objects.get_for_model(Book)

        # Get or create permissions
        add_book = Permission.objects.get_or_create(
            codename='can_add_book',
            name='Can add book',
            content_type=book_content_type,
        )[0]
        edit_book = Permission.objects.get_or_create(
            codename='can_edit_book',
            name='Can edit book',
            content_type=book_content_type,
        )[0]
        delete_book = Permission.objects.get_or_create(
            codename='can_delete_book',
            name='Can delete book',
            content_type=book_content_type,
        )[0]
        view_book = Permission.objects.get_or_create(
            codename='can_view_book_details',
            name='Can view book details',
            content_type=book_content_type,
        )[0]

        # Assign permissions to groups
        # Admin gets all permissions
        admin_group.permissions.add(add_book, edit_book, delete_book, view_book)

        # Librarian can add, edit, and view books
        librarian_group.permissions.add(add_book, edit_book, view_book)

        # Members can only view books
        member_group.permissions.add(view_book)

        self.stdout.write(self.style.SUCCESS('Successfully set up groups and permissions'))