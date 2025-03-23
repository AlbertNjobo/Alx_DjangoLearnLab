from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']  # Exclude 'author' as it will be set automatically

    def save(self, commit=True, user=None):
        post = super().save(commit=False)
        if user:
            post.author = user  # Set the author to the logged-in user
        if commit:
            post.save()
        return post
