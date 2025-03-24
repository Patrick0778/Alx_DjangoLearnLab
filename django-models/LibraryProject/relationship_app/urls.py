from django.urls import path
from .views.auth_views import login_view, logout_view, register
from .views.admin_view import admin_view
from .views.librarian_view import librarian_view
from .views.member_view import member_view
from .views.book_views import (
    BookCreateView, 
    BookUpdateView, 
    BookDeleteView,
    book_list,
    book_detail,
    LibraryDetailView
)

app_name = 'relationship_app'

urlpatterns = [
    # Authentication URLs
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    
    # Role-based dashboard URLs
    path('admin/dashboard/', admin_view, name='admin_dashboard'),
    path('librarian/dashboard/', librarian_view, name='librarian_dashboard'),
    path('member/dashboard/', member_view, name='member_dashboard'),
    
    # Book management URLs with permissions
    path('books/', book_list, name='book_list'),
    path('books/add/', BookCreateView.as_view(), name='book_add'),
    path('books/<int:pk>/edit/', BookUpdateView.as_view(), name='book_edit'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),
    path('books/<int:pk>/', book_detail, name='book_detail'),
    
    # Library URLs
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]