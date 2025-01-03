from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models.models import Post, Tag
from .serializers.serializers import PostSerializer


class TagView(APIView):
    """
    Supports:
      - Single tag in the URL path: /api/posts/tag/<tag_name>/
      - Multiple tags as query parameters: /api/posts/tags/?tags=Python&tags=Programming
    """

    def get(self, request, tag_name=None, *args, **kwargs):
        # Check if a single tag is provided in the URL
        if tag_name:
            posts = Post.objects.filter(tags__name=tag_name).distinct()
            if not posts.exists():
                return Response({"Message": f"No posts found with the tag '{tag_name}'."},
                                status=status.HTTP_404_NOT_FOUND)
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Check if multiple tags are provided as query parameters
        tag_names = request.query_params.getlist('tags')
        if tag_names:
            posts = Post.objects.filter(tags__name__in=tag_names).distinct()
            if not posts.exists():
                return Response(
                    {"Message": f"No posts found matching the tags: {', '.join(tag_names)}."},
                    status=status.HTTP_404_NOT_FOUND)
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # No tags provided in either path or query parameters
        return Response(
            {"Message": "No tags provided. Use a single tag in the URL path or multiple tags as query parameters."},
            status=status.HTTP_400_BAD_REQUEST
        )
