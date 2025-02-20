from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # Authentication URLs
    path("register/", views.register, name="register"),
    path("login/", LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),

    # Book Management with Permissions
    path("books/", views.list_books, name="list_books"),
    path("add_book/", views.add_book, name="add_book"),  # Fix: Ensuring "add_book/" path is correct
    path("edit_book/<int:book_id>/", views.edit_book, name="edit_book"),  # Fix: Ensuring "edit_book/" path is correct
    path("delete_book/<int:book_id>/", views.delete_book, name="delete_book"),  # Already correct

    # Library Details
    path("library/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"),

    # Role-Based Views
    path("admin-view/", views.admin_view, name="admin_view"),
    path("librarian-view/", views.librarian_view, name="librarian_view"),
    path("member-view/", views.member_view, name="member_view"),
]
