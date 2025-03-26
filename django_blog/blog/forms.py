from django import forms
from taggit.forms import TagWidget
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # Include 'tags' directly
        widgets = {
            'tags': TagWidget(attrs={'placeholder': 'Comma-separated tags'}),  # Use TagWidget directly
        }
        help_texts = {
            'tags': "Add tags separated by commas.",
        }

    def save(self, commit=True, user=None):
        post = super().save(commit=False)
        if user:
            post.author = user  # Set the author to the logged-in user
        if commit:
            post.save()
        return post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
