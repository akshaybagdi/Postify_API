import logging

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status, request
from .models.models import Post, Tag  # Assuming you have a Tag model for tags
from .serializers.serializers import PostSerializer

logger = logging.getLogger(__name__)


class PostID():
    @staticmethod
    def get_post_by_id(post_id):
        if not post_id:
            logger.error("Post ID is required but not provided.")
            return Response({"Error": "Post ID is required in the payload."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            post = Post.objects.get(id=post_id)
            logger.info(f"Post retrieved successfully with ID {post_id}")
            return post  # Return the post instance for further processing
        except Post.DoesNotExist:
            logger.warning(f"Post with ID {post_id} not found.")
            return Response({"Error": f"Post with ID {post_id} not found."}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def delete_post_by_id(post_id):
        logger.info(f"Attempting to delete post with ID: {post_id}")
        # Retrieve the post using the helper method
        post = PostID.get_post_by_id(post_id)
        if isinstance(post, Response):
            logger.error(f"Failed to delete post. Post with ID {post_id} not found.")
            return post  # Return error Response directly
        try:
            post.delete()
            logger.info(f"Post with ID {post_id} successfully deleted.")
            return Response({"message": "Post successfully deleted."}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"An error occurred while deleting post with ID {post_id}: {str(e)}")
            return Response({"error": "An error occurred while deleting the post."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # class PostID:
    @staticmethod
    def update_post(post_id, data):
        post = PostID.get_post_by_id(post_id)
        if isinstance(post, Response):
            logger.error(f"Failed to update post. Post with ID {post_id} not found.")
            return post
        try:
            serializer = PostSerializer()
            title = data.get('title')
            content = data.get('content')
            category = data.get('category')
            is_published = data.get('is_published')
            rating = data.get('rating')
            website = data.get('website')
            # tags=data.get('name')

            if title is not None:
                title = serializer.validate_title(title)
            if rating is not None:
                rating = serializer.validate_rating(rating)
            if is_published is not None:
                is_published = serializer.validate_is_published(is_published)
            # if category is not None:
            #     category = serializer.validate_category(category)
            post.title = title
            post.content = content
            post.category = category
            post.is_published = is_published
            post.rating = rating
            post.website = website
            # post.tags=tags
            post.save()
            return post
        except ValidationError as e:  # Catch validation errors and return them in the response
            logger.error(f"Validation error during post update for post ID {post_id}: {e.detail}")
            return Response({"Error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error during post update for post ID {post_id}: {str(e)}", exc_info=True)
            return Response({"Error": "An unexpected error occurred while updating the post."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
