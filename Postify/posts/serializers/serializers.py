import logging
from rest_framework import serializers
from ..models.models import Post, Tag
from django.apps import apps


# logger = logging.getLogger(__name__)


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for displaying comments on a post."""
    user = serializers.StringRelatedField()  # Display the username of the commenter

    class Meta:
        Comment = apps.get_model('comments',
                                 'Comment')  # Dynamic import. Used this because directly import is not working
        model = Comment
        fields = ['user', 'content']


class LikeSerializer(serializers.ModelSerializer):
    """Serializer for displaying likes on a post."""
    user = serializers.StringRelatedField()  # Display the username of the liker

    class Meta:
        Like = apps.get_model('likes', 'Like')  # Dynamic import. Used this because directly import is not working
        model = Like
        fields = ['user']


class TagSerializer(serializers.ModelSerializer):
    """Serializer for the Tag model."""

    class Meta:
        model = Tag
        fields = ['name']


class PostSerializer(serializers.ModelSerializer):
    """Serializer for the Post model."""
    author = serializers.CharField(source='author.username', read_only=True)  # Fetch the username of the author
    # comments = CommentSerializer(many=True, read_only=True)  # Nested comments
    comments = serializers.SerializerMethodField()  # Custom field for comments
    likes = LikeSerializer(many=True, read_only=True)  # Nested likes
    like_count = serializers.SerializerMethodField()  # Display the total number of likes
    tags = serializers.ListField(
        child=serializers.DictField(), write_only=True)
    tags_used = serializers.SerializerMethodField(read_only=True)  # Display tags as names

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'category', 'is_published', 'rating', 'website', 'tags',
                  'comments', 'like_count', 'likes', "tags_used"]

    def get_comments(self, obj):
        """Get all comments for the post."""
        comments_qs = obj.comments.all()
        if comments_qs.exists():
            return [
                {"content": comment.content, "username": comment.user.username}
                for comment in comments_qs
            ]
        # logger.info(f"No comments found for Post ID {obj.id}")
        return "This Post Has No Comments"

    def get_like_count(self, obj):
        """Get the total number of likes for the post."""
        like_count = obj.likes.count()
        # logger.info(f"Post ID {obj.id} has {like_count} likes")
        return like_count

    def get_tags_used(self, obj):
        """Display tags as a list of names."""
        return [tag.name for tag in obj.tags.all()]

    def create(self, validated_data):
        print("create_tag")
        tags_data = validated_data.pop('tags', [])  # Extract tags data
        post = Post.objects.create(**validated_data)  # Create the post

        for tag_data in tags_data:  # joining tags with the post
            print("helllllooooooooooo")
            tag_name = tag_data.get("name")  # Extract the tag name
            tag, created = Tag.objects.get_or_create(name=tag_name)  # Create or retrieve the tag
            print(tag, "taaagggggg")
            post.tags.add(tag)  # Associate the tag with the post
        return post
        # Associate tags with the post

    def validate_title(self, value):
        # print("you are in the serializer function")
        if len(value) <= 0:
            raise serializers.ValidationError("Title cannot be Null")
        elif len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long.")
        return value


    def validate_rating(self, value):
        """Validate the rating field."""
        try:
            value = float(value)
        except ValueError:
            raise serializers.ValidationError("Rating must be a number between 1 and 5.")
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate_is_published(self, value):
        """Validate the is_published field."""
        if not isinstance(value, bool):
            raise serializers.ValidationError("is_published must be a boolean value. i.e true and false")
        return value
