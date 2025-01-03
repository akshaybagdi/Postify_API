import logging
from rest_framework import generics, permissions, status, viewsets, filters
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models.models import Comment
from .serializers.serializers import CommentSerializer
from .utlis import CommentID
from django.apps import apps
from core import UserPermission

# Configure logging
logger = logging.getLogger(__name__)


class CommentList(generics.ListAPIView, viewsets.GenericViewSet):
    """
    API to list comments.
    """
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering = ['-id']

    def get_queryset(self):
        comment_id = self.request.data.get("id")
        logger.info(f"Fetching comments with ID: {comment_id}" if comment_id else "Fetching all comments.")

        if comment_id:
            queryset = Comment.objects.filter(id=comment_id)
            if not queryset.exists():
                logger.error(f"No comments found with ID: {comment_id}")
                raise NotFound("No comment found with the given ID.")
            return queryset
        return Comment.objects.all()


class CommentCreate(generics.CreateAPIView, viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.request.data.get('post_id')  # Get post_id from request payload
        logger.info(f"Post ID: {post_id}")
        logger.info(f"User {self.request.user} is attempting to create a comment on post ID: {post_id}.")

        # Dynamically fetch the Post model using apps.get_model
        Post = apps.get_model('posts', 'Post')

        # Ensure the post exists
        post = Post.objects.filter(id=post_id).first()
        if not post:
            raise NotFound(detail="Post not found.")

        # Save the comment with user and post
        serializer.save(user=self.request.user, post=post)
        logger.info(f"Comment successfully created by user {self.request.user} on post ID {post_id}.")

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)


class CommentUpdate(generics.UpdateAPIView, viewsets.GenericViewSet):
    """
    API to update a comment.
    """
    # queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, UserPermission]

    def update(self, request, *args, **kwargs):
        comment_id = request.data.get('id')
        logger.info(f"User {request.user} attempting to update comment ID: {comment_id}.")
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            logger.error(f"Comment ID {comment_id} not found.")
            return Response({"Error": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)
        updated_comment = CommentID.update_comment(comment_id, request.data)
        if isinstance(updated_comment, Response):
            logger.error(f"Error updating comment ID: {comment_id}.")
            return updated_comment

        # serializer = self.get_serializer(updated_comment)
        serializer = self.get_serializer(comment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f"Comment ID {comment_id} successfully updated.")
        return Response({"Message": "Comment updated successfully.", "comment": serializer.data},
                        status=status.HTTP_200_OK)


class CommentDelete(generics.DestroyAPIView, viewsets.GenericViewSet):
    """
    API to delete a comment.
    """
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, UserPermission]

    def destroy(self, request, *args, **kwargs):
        comment_id = request.data.get('id')
        logger.info(f"User {request.user} attempting to delete comment ID: {comment_id}.")
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            logger.error(f"Comment ID {comment_id} not found.")
            return Response({"Error": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)
        deletion_response = CommentID.delete_comment_by_id(comment_id)
        if isinstance(deletion_response, Response):
            logger.error(f"Error deleting comment ID: {comment_id}.")
            return deletion_response

        logger.info(f"Comment ID {comment_id} successfully deleted.")
        return Response({"message": "Comment successfully deleted."}, status=status.HTTP_200_OK)
