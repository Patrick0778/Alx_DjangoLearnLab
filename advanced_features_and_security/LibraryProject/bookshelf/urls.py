from django.urls import path
from . import views

app_name = 'bookshelf'

urlpatterns = [
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('change-password/', views.change_password, name='change_password'),
    
    # Role-based dashboard URLs
    path('admin/dashboard/', views.admin_view, name='admin_dashboard'),
    path('librarian/dashboard/', views.librarian_view, name='librarian_dashboard'),
    path('member/dashboard/', views.member_view, name='member_dashboard'),
    
    # Book management URLs with permissions
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.BookCreateView.as_view(), name='book_add'),
    path('books/<int:pk>/edit/', views.BookUpdateView.as_view(), name='book_edit'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    
    # Library URLs
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    
    # Add the example form URL pattern
    path('form-example/', views.form_example, name='form_example'),
]