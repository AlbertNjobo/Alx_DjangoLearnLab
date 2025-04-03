from django.shortcuts import render
from rest_framework import viewsets, permissions, pagination, filters, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from .models import Post, Comment, Like
from django.db.models import Count
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from notifications.models import Notification  # Import Notification model
from django.contrib.contenttypes.models import ContentType

# Create your views here.

#-- Custom Pagination Class ---
class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

#-- Post ViewSet ---

class PostViewSet(viewsets.ModelViewSet):
    """ViewSet for managing posts"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Pass the author explicitly
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = generics.get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            # Generate a notification for the post author
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='liked your post',
                target=post,
            )
            return Response({'message': 'Post liked'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Already liked'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        post = generics.get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(post=post, user=request.user).first()
        if like:
            like.delete()
            return Response({'message': 'Post unliked'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'Not liked yet'}, status=status.HTTP_400_BAD_REQUEST)

#-- Comment ViewSet ---

class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for managing comments"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Comment.objects.all()
        post_id = self.request.query_params.get('post_id', None)
        if post_id is not None:
            queryset = queryset.filter(post__id=post_id)
        return queryset

    def perform_create(self, serializer):
        # Post needs to be determined from context or URL if creating directly
        # This setup assumes comment creation mostly happens via the PostViewSet action
        # If direct creation at /api/comments/ is needed, need a way to specify the post
        # For now, let's assume creation mainly happens via /api/posts/{pk}/comments/
        # which is handled by PostViewSet's list_create_comments action
        # and the serializer context there.
         if 'post' in self.get_serializer_context():
             serializer.save(author=self.request.user, post=self.get_serializer_context()['post'])
         else:
             # Handle cases where 'post' might not be in context - raise error or require post_id in request data
             # For simplicity, let's assume it's always provided via context for now.
             serializer.save(author=self.request.user)

    # Override get_serializer_context to pass request and potentially post
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        # If accessing comments directly, we might not have 'post' unless passed via URL or data
        # This context is primarily useful when the ViewSet is used directly
        return context

    # Allow retrieving/editing/deleting single comments via posts/{pk}/comments/{comment_pk}
    @action(detail=True, methods=['get', 'put', 'patch', 'delete'], permission_classes=[permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly], url_path='manage')
    def manage_comment(self, request, pk=None):
        comment = self.get_object() # This pk refers to the comment id
        if request.method == 'GET':
            serializer = self.get_serializer(comment)
            return Response(serializer.data)
        elif request.method in ['PUT', 'PATCH']:
            serializer = self.get_serializer(comment, data=request.data, partial=request.method=='PATCH')
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        elif request.method == 'DELETE':
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

#-- Feed View ---

class FeedView(APIView):
    """API view to generate a feed of posts from followed users."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        following_users = request.user.following.all()
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)