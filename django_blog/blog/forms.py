from django import forms
from taggit.forms import TagWidget
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  
        widgets = {
            'tags': TagWidget(),  # Ensure TagWidget() is inside the widgets dictionary
        }

    def save(self, commit=True, user=None):
        post = super().save(commit=False)
        if user:
            post.author = user  # Set the author to the logged-in user
        if commit:
            post.save()
        return post
