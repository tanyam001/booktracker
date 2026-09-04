from django.urls import path
from .views import (
    BookDetailView,
    MyBookListView, 
    HomePageView, 
    AboutView, 
    register, 
    ProfileUpdateView, 
    BookCreateView, 
    BookUpdateView, 
    BookDeleteView,
    add_comment,
    delete_comment
)
from django.contrib.auth import views


urlpatterns = [
    path("", HomePageView.as_view(), name="book_list"),
    path("about/", AboutView.as_view(), name = "about"),
    path("my_books/", MyBookListView.as_view(), name = "my_books"),
    path("<int:pk>/", BookDetailView.as_view(), name = "book_detail"),
    path("<int:pk>/edit/", BookUpdateView.as_view(), name = "book_update"),
    path("<int:pk>/delete/", BookDeleteView.as_view(), name = "book_delete"),
    path("register/", register, name = "register"),
    path("login/", views.LoginView.as_view(template_name = "login.html"), name = "login"),
    path("logout/", views.LogoutView.as_view(), name = "logout"),
    path("profile/", ProfileUpdateView.as_view(), name = "profile"),
    path("add/", BookCreateView.as_view(), name = "book_add"),
    path("<int:pk>/comment/", add_comment, name = "add_comment"),
    path("comment/<int:pk>/delete/", delete_comment, name = "delete_comment")
]