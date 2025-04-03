from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for the author of a post"""
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'profile_picture')

class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments on a post"""
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'post','author', 'content', 'created_at', 'updated_at')
        read_only_fields = ('id', 'author','created_at', 'updated_at','post')

        # -- Set the author to the current user in the view --
        def create(self, validated_data):

            post = self.context['post']
            author = self.context['request'].user
            comment = Comment.objects.create(post=post, author=author, **validated_data)
            return comment
        
class PostSerializer(serializers.ModelSerializer):
    """Serializer for posts"""
    author = AuthorSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'content', 'created_at', 'updated_at', 'comments', 'comment_count')
        read_only_fields = ('id', 'author', 'created_at', 'updated_at', 'comments', 'comment_count')

        def get_comment_count(self, obj):
            return obj.comments.count()
        
    def create(self, validated_data):
        author = self.context['request'].user
        post = Post.objects.create(author=author, **validated_data)
        return post
