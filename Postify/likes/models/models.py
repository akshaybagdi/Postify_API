from django.db import models
from django.utils.translation import gettext_lazy as _
# from posts.models import Post  # Import the Post model
from django.contrib.auth.models import User  # Replace this with your custom user model if needed


class Like(models.Model):
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='likes', verbose_name=_("Post"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    class Meta:
        db_table = "Postify_like"
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")
        unique_together = ('post', 'user')  # Ensures a user can like a post only once

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"
