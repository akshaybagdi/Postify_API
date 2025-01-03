from django.db import models
from django.utils.translation import gettext_lazy as _
# from .models import Post  # Import the Post model
from django.contrib.auth.models import User  # Replace this with your custom user model if needed


class Comment(models.Model):
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='comments', verbose_name=_("Post"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="The user who authored this comment",
                             verbose_name=_("User"))
    content = models.TextField(_('Content'), help_text="The content of the comment")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time when the comment was created",
                                      verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, help_text="The date and time when the comment was last updated",
                                      verbose_name=_("Updated At"))

    class Meta:
        db_table = "Postify_comment"
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"
