from django import forms
from .models import Post
from .models import Comment

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

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
