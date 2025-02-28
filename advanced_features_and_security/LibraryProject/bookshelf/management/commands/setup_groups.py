from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Library, Book

class Command(BaseCommand):
    help = 'Creates default groups and assigns permissions'

    def handle(self, *args, **options):
        # Create groups
        admin_group, _ = Group.objects.get_or_create(name='Admins')
        editor_group, _ = Group.objects.get_or_create(name='Editors')
        viewer_group, _ = Group.objects.get_or_create(name='Viewers')

        # Get content types
        library_content_type = ContentType.objects.get_for_model(Library)
        book_content_type = ContentType.objects.get_for_model(Book)

        # Get all permissions
        library_permissions = Permission.objects.filter(content_type=library_content_type)
        book_permissions = Permission.objects.filter(content_type=book_content_type)

        # Assign permissions to Admin group
        for perm in library_permissions:
            admin_group.permissions.add(perm)
        for perm in book_permissions:
            admin_group.permissions.add(perm)

        # Assign permissions to Editor group
        editor_perms = [
            'can_edit_library', 'can_view_library', 'can_manage_books',
            'can_edit_book', 'can_view_book_details'
        ]
        for perm in Permission.objects.filter(codename__in=editor_perms):
            editor_group.permissions.add(perm)

        # Assign permissions to Viewer group
        viewer_perms = ['can_view_library', 'can_view_book_details']
        for perm in Permission.objects.filter(codename__in=viewer_perms):
            viewer_group.permissions.add(perm)

        self.stdout.write(self.style.SUCCESS('Successfully set up groups and permissions'))