from rest_framework.response import Response
from rest_framework import status
from .models.models import Comment


class CommentID:
    @staticmethod
    def get_comment_by_id(comment_id):
        """
        Retrieve a comment by its ID.
        :param comment_id: The ID of the comment to retrieve
        :return: Comment instance or Response with error message
        """
        if not comment_id:
            return Response({"Error": "Comment ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            comment = Comment.objects.get(id=comment_id)
            return comment
        except Comment.DoesNotExist:
            return Response({"Error": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def delete_comment_by_id(comment_id):
        """
        Delete a comment by its ID.
        :param comment_id: The ID of the comment to delete
        :return: Response object with success or error message
        """
        comment = CommentID.get_comment_by_id(comment_id)

        # If retrieval returns an error Response, return it directly
        if isinstance(comment, Response):
            return comment

        comment.delete()
        return Response({"message": "Comment successfully deleted."}, status=status.HTTP_200_OK)

    @staticmethod
    def update_comment(comment_id, data):
        """
        Update a comment by its ID with the provided data.
        :param comment_id: The ID of the comment to update
        :param data: The data to update the comment with
        :return: Updated comment instance or Response object if errors occur
        """
        comment = CommentID.get_comment_by_id(comment_id)

        # If retrieval returns an error Response, return it directly
        if isinstance(comment, Response):
            return comment

        # Update the fields dynamically
        for field, value in data.items():
            setattr(comment, field, value)

        comment.save()
        return comment
