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

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  # Link to Post
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to User
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"