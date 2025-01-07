from rest_framework import serializers
from ..models.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model.
    Handles creating, retrieving, and validating comment data.
    """
    user = serializers.StringRelatedField(read_only=True)  # Display the username in a human-readable form
    post = serializers.PrimaryKeyRelatedField(read_only=True)  # Display the post ID

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'content', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']  # Fields that cannot be modified


    def to_internal_value(self, data):
        """Override to bypass default blank validation.
        BaseSerializer class that DRF calls during deserialization
        to validate and transform input data
        into Python native types"""
        content = data.get('content')
        if content is None or content.strip() == '':
            raise serializers.ValidationError({'content': "Content cannot be empty "})
        return super().to_internal_value(data)

    def validate_content(self, value):
        """Ensure the content field is not empty or null."""
        if not value or not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        return value


