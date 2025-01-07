from rest_framework.exceptions import ValidationError
import logging
from .serializers.serializers import PostSerializer

logger = logging.getLogger(__name__)


def validate_fields(func):
    """Custom decorator to validate post data before creating or updating."""
    def wrapper(self, request, *args, **kwargs):
        # Extract data from the request
        data = request.data
        serializer = PostSerializer(data=data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)  # Raise validation error if data is invalid

        # If validation passes, continue to the original function
        return func(self, request, *args, **kwargs)

    return wrapper
