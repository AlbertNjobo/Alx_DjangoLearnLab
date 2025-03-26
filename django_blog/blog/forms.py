from django import forms
from taggit.forms import TagField, TagWidget
from .models import Post, Comment

class PostForm(forms.ModelForm):
    tags = TagField(widget=TagWidget(), required=False)  # Ensure TagWidget() is used directly

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # Ensure 'tags' is explicitly listed

    def save(self, commit=True, user=None):
        post = super().save(commit=False)
        if user:
            post.author = user  # Set the author to the logged-in user
        if commit:
            post.save()
        return post
