from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView, DeleteView, ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, ProfileForm, CommentForm

from .models import Book, Profile, Comment

from django.contrib.auth.decorators import login_required


# shows the home page

class HomePageView(ListView):
    model = Book
    template_name = "book_list.html"
    context_object_name = "books"

# add books

class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    fields = [
    "cover",
    "title",
    "author",
    "genre",
    "total_pages",
    "pages_read",
    "rating",
    "status",
    "date_started",
    "date_finished",
    "notes",
    ]
    template_name = "book_add.html"
    success_url = "/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# shows all the books added to the website

class BookListView(ListView):
    model = Book
    template_name = "book_list.html"
    context_object_name = "books"

# shows only the user's book to them

class MyBookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = "my_books.html"
    context_object_name = "books"

    def get_queryset(self):
        return Book.objects.filter(user = self.request.user)

# shows a specific book's info

class BookDetailView(DetailView):
    model = Book
    template_name = "book_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.all()
        return context

# enables editing for the logged in user

class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    fields = [
        "cover",
        "title",
        "author",
        "genre",
        "total_pages",
        "pages_read",
        "rating",
        "status",
        "date_started",
        "date_finished",
        "notes",
    ]
    template_name = "book_update.html"

    def test_func(self):
        book = self.get_object()
        return book.user == self.request.user

    def get_success_url(self):
        return reverse_lazy(
            "book_detail",
            kwargs = {"pk": self.object.pk}
        )

# enables deleting for the logged in user

class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    template_name = "book_delete.html"
    success_url = reverse_lazy("book_list")

    def test_func(self):
        book = self.get_object()
        return book.user == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["commments"] = self.object.comments.all()
        context["forms"] = CommentForm()
        return context

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            Profile.objects.create(user = user)
            login(request, user)
            return redirect("book_list")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form":form})

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "profile.html"

    def get_object(self):
        return self.request.user.profile

    def get_success_url(self):
        return reverse_lazy("book_list")


class AboutView(TemplateView):
    template_name = "about.html"


@login_required
def add_comment(request, pk):
    book = Book.objects.get(pk = pk)

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit = False)
            comment.user = request.user
            comment.book = book
            comment.save()

    return redirect("book_detail", pk = book.pk)

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk = pk)

    if comment.user == request.user:
        book_pk = comment.book.pk
        comment.delete()
        return redirect("book_detail", pk=book_pk)

    return redirect("book_detail", pk = comment.book.pk)