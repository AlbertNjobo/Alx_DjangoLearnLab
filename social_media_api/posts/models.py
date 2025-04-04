# posts/models.py
from django.db import models
from django.conf import settings # To link to the custom User model

class Post(models.Model):
    """ Represents a single post by a user. """
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at'] # Default order: newest first

    def __str__(self):
        return f"'{self.title}' by {self.author.username}"

class Comment(models.Model):
    """ Represents a comment on a post. """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at'] # Default order: oldest first for comments

    def __str__(self):
        return f"Comment by {self.author.username} on '{self.post.title}'"

class Like(models.Model):
    """Represents a like on a post."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')  # Prevent duplicate likes
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} liked '{self.post.title}'"