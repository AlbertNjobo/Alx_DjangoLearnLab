from django.db import models
from django.contrib.auth.models import User  # Import User model

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)  # Updated max_length to 200
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Added author field

    def __str__(self):
        return self.title