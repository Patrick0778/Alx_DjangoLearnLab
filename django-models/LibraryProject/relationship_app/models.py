from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Role choices tuple
ROLE_CHOICES = [
    ('ADMIN', 'Admin'),
    ('LIBRARIAN', 'Librarian'),
    ('MEMBER', 'Member'),
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='MEMBER')

    def __str__(self):
        return f"{self.user.username} - {self.role}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    class Meta:
        permissions = [
            ('can_add_book', 'Can add book'),
            ('can_edit_book', 'Can edit book'),
            ('can_delete_book', 'Can delete book'),
            ('can_view_book_details', 'Can view book details'),
        ]

    def __str__(self):
        return self.title

class Library(models.Model):
    name = models.CharField(max_length=200)
    books = models.ManyToManyField(Book, related_name='libraries')

    def __str__(self):
        return self.name

class Librarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)

    def __str__(self):
        return f"Librarian at {self.library.name}"
