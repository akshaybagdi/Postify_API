import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from django.apps import apps
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers.serializers import LikeSerializer
from .models.models import Like

logger = logging.getLogger(__name__)


class LikeViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        """Handle liking a post using the payload."""
        user = request.user
        logger.info(f"User {user} is attempting to like a post.")

        # Validate and get post_id from request data
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            post_id = serializer.validated_data['post_id']
        else:
            logger.error("Invalid payload: %s", serializer.errors)
            return Response({"message": "Invalid data.", "errors": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        # Dynamic Import due to circular path/module error
        Post = apps.get_model('posts', 'Post')
        post = Post.objects.filter(id=post_id).first()

        if not post:
            logger.error(f"Post with ID {post_id} not found.")
            raise NotFound("Post not found")

        # Check if the user already liked the post
        if Like.objects.filter(user=user, post=post).exists():
            logger.warning(f"User {user} has already liked post with ID {post_id}.")
            return Response({"message": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new Like with the authenticated user
        Like.objects.create(user=user, post=post)
        logger.info(f"User {user} successfully liked post with ID {post_id}.")
        return Response({"message": "Post liked successfully."}, status=status.HTTP_201_CREATED)

    def destroy(self, request):
        """Handle unliking a post using the payload."""
        user = request.user
        logger.info(f"User {user} is attempting to unlike a post.")

        # Validate and get post_id from request data
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            post_id = serializer.validated_data['post_id']
        else:
            logger.error("Invalid payload: %s", serializer.errors)
            return Response({"message": "Invalid data.", "errors": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        Post = apps.get_model('posts', 'Post')
        post = Post.objects.filter(id=post_id).first()

        if not post:
            logger.error(f"Post with ID {post_id} not found.")
            raise NotFound("Post not found")

        # Check if the user has already liked the post
        like = Like.objects.filter(user=user, post=post).first()
        if not like:
            logger.warning(f"User {user} has not liked post with ID {post_id}.")
            return Response({"message": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Remove the like
        like.delete()
        logger.info(f"User {user} successfully unliked post with ID {post_id}.")
        return Response({"message": "Post unliked successfully."}, status=status.HTTP_200_OK)
