from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    year = models.IntegerField(null=True, blank=True)

    description = models.TextField()

    pdf = models.FileField(upload_to='books/', null=True, blank=True)

    downloads = models.IntegerField(default=0)

    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Bookmark(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
     
    def __str__(self):
        return f"{self.user.username} - {self.book.title}"