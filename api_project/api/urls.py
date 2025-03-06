from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, BookList

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

# The API URLs are now determined automatically by the router
urlpatterns = [
    # Route for the BookList view (ListAPIView)
    path('books/', BookList.as_view(), name='book-list'),
    
    # Include the router URLs for BookViewSet (all CRUD operations)
    path('', include(router.urls)),  # This includes all routes registered with the router
]