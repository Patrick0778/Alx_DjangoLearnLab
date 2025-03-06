from django.shortcuts import render
from rest_framework import viewsets, generics, permissions
from .models import Book
from .serializers import BookSerializer

# Create your views here.

class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed or edited.
    Requires authentication for all operations.
    Only staff users can create, update or delete books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        - List and Retrieve operations are allowed for any authenticated user
        - Create, Update, and Delete operations require staff privileges
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

class BookList(generics.ListAPIView):
    """
    API endpoint that allows books to be viewed.
    This endpoint is read-only and available to all authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

# Create a custom permission for demonstration
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin users to edit objects.
    Read permissions are allowed to any authenticated user.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Write permissions are only allowed to admin users
        return request.user and request.user.is_staff
