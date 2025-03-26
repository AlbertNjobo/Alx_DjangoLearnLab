from django import forms
from .models import Post, Tag
from .models import Comment

class PostForm(forms.ModelForm):
    tags = forms.CharField(required=False, help_text="Comma-separated tags")

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # Exclude 'author' as it will be set automatically

    def save(self, commit=True, user=None):
        post = super().save(commit=False)
        if user:
            post.author = user  # Set the author to the logged-in user
        tags = self.cleaned_data['tags']
        if commit:
            post.save()
            tag_names = [tag.strip() for tag in tags.split(',') if tag.strip()]
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                post.tags.add(tag)
        return post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
