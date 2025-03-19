from django.urls import path
from django.contrib import admin
from api.views import BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView  # Import your views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/update/<int:pk>/', BookUpdateView.as_view(), name='book-update'),
    path('books/delete/<int:pk>/', BookDeleteView.as_view(), name='book-delete'),
]
