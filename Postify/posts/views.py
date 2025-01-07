import logging
from rest_framework import mixins, viewsets, status, filters, permissions
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from core import UserPermission
from .models.models import Post
from .pagniations.pagniations import CustomPagination
from .serializers.serializers import PostSerializer
from .utlis import PostID
from .decorators import validate_fields

logger = logging.getLogger(__name__)

"""
Using mixins allows us to add specific functionality (e.g., list, delete,retrieve) to views.
viewsets.GenericViewSet provides the base functionality for creating custom views with mixins.
"""


class PostList(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.all()  # Fetch all Post objects
    serializer_class = PostSerializer  # Serialize Post model data
    pagination_class = CustomPagination  # Paginate the results
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]  # Enable search and ordering
    search_fields = ['title', 'content']  # Searchable fields
    # ordering_fields = ['is_published']  # Fields to order by
    # ordering = ['-is_published']  # Default ordering (newest first)
    authentication_classes = [JWTAuthentication]  # Use JWT for authentication
    permission_classes = [IsAuthenticated]  # Authenticated users can write; others can only read


class PostUserDetail(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        post_id = request.data.get('id')  # Get the ID from the request payload
        post = PostID.get_post_by_id(post_id)  # Directly call the static method of PostH
        if isinstance(post, Response):  # If the helper(PostID) function returns a Response (error), return it directly
            return post
        serializer = self.get_serializer(post)  # Otherwise, process the post instance and return the response
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostUserUpdate(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, UserPermission]

    def update(self, request, *args, **kwargs):
        logger.info("Received update request.")
        post_id = request.data.get('id')  # Extract post ID from payload
        data = request.data  # Full payload
        try:
            updated = PostID.update_post(post_id, data)  # Call the `update_post` method
            if isinstance(updated, Response):  # If the helper method returns a Response, return it directly
                logger.error(f"Post update failed for ID {post_id}: {updated.data}")
                return updated
            logger.info(f"Post with ID {post_id} updated successfully.")
            self.check_object_permissions(request, updated)
            serializer = self.get_serializer(updated)  # Serialize the updated post
            # print(serializer)
            logger.info(f"{serializer}")
            response = Response({"Message": "Post updated successfully.", "post": serializer.data},
                                status=status.HTTP_200_OK)
            logger.info(f"Response for update request: {response.data}")
            return response
        except PermissionDenied as e:
            logger.warning(f"Permission denied for user {request.user.username} to update post {post_id}")
            return Response({"Message": "Editing post is restricted to the User only"},
                            status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            # Log unexpected errors
            logger.error(f"Unexpected error during post update for Post ID {post_id}: {str(e)}", exc_info=True)
            return Response({"Error": "An unexpected error occurred while updating the post."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostUserDestroy(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    permission_classes = [permissions.IsAuthenticated, UserPermission]

    def delete(self, request, *args, **kwargs):
        post_id = request.data.get('id')  # Get the ID from the request payload
        try:
            try:
                delete_post = Post.objects.get(id=post_id)
            except Post.DoesNotExist:
                logger.error(f"Post with ID {post_id} not found.")
                return Response({"Error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
            self.check_object_permissions(request, delete_post)
            response = PostID.delete_post_by_id(post_id)  # Call the helper method to delete the post
            logger.info(f"Post with ID {post_id} successfully deleted.")
            return response  # Return the response from the helper method
        except PermissionDenied as e:
            logger.warning(f"Permission denied for user {request.user.username} to update post {post_id}")
            return Response({"Message": "Delete post is restricted to the User only"}, status=status.HTTP_403_FORBIDDEN)


class PostUserCreate(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @validate_fields  # Apply the custom validation decoratora
    def create(self, request, *args, **kwargs):
        try:

            author = request.user if request.user.is_authenticated else None # Check if the user is authenticated, and assign the author field
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(): # Validate serializer and add the authenticated author
                post = serializer.save(author=author)  # Assign the author (authenticated user)
                logger.info(f"Post created: {post}")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            logger.error(f"Validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e: # Handle validation error raised in the decorator
            logger.error(f"Validation error: {e.detail}")
            return Response({"Error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e: # Handle unexpected errors
            logger.error(f"Unexpected error during post creation: {str(e)}", exc_info=True)
            return Response({"Error": f"An unexpected error occurred: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
