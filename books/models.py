from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView, DeleteView, ListView, DetailView
from django.urls import reverse_lazy

# the model

class Book(models.Model):
    STATUS_CHOICE = [
        ("want", "Want to read"),
        ("reading", "Currently reading"),
        ("finished", "Finished"),
    ]
    cover = models.ImageField(upload_to="book_cover/")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=100, blank=True)
    total_pages = models.PositiveIntegerField()
    pages_read = models.PositiveIntegerField(default=0)
    rating = models.PositiveIntegerField(null = True, blank = True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICE,
        default="want"
    )
    date_started = models.DateField(null =True, blank=True)
    date_finished = models.DateField(null = True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.title

# enables adding comments under books of different users

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(
        Book, 
        on_delete=models.CASCADE,
        related_name= "comments"
        )
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

# set profile picture while registering

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        default = "profile_pictures/default.jpg",
        blank=True
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"