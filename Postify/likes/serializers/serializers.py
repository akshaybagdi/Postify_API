from django.apps import apps
from rest_framework import serializers
from ..models.models import Like


class LikeSerializer(serializers.ModelSerializer):
    # Post = apps.get_model('posts', 'Post')
    # post_id is automatically managed by the ForeignKey relationship
    post_id = serializers.IntegerField(required=True)  # Input: post_id
    title = serializers.CharField(source='post.title', read_only=True)


    class Meta:
        model = Like
        fields = ['id', 'post_id', 'title', 'created_at']  # Exclude user from the payload
        read_only_fields = ['user', 'created_at']
