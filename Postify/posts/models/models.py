from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    title = models.CharField(_('Title'), max_length=50, help_text=_(
        "The title of the post (max 200 characters)."), blank=False)  # A title for the post (text)

    content = models.TextField(_('Content'), max_length=200, help_text=_(
        "The main content of the post. Use rich text for full details."), )  # Content of the post (long text)

    created_at = models.DateTimeField(auto_now_add=True, help_text=_(
        "The date and time when the post was created."), )  # Date when post was created

    updated_at = models.DateTimeField(auto_now=True, help_text=_(
        "The date and time when the post was last updated."), )  # Date when post was last updated

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts',
                               help_text=_(
                                   "The author of this post (related to User model)."))  # Author of the post (related to User model)

    # Choice field for post category (Example: Blog, News, etc.)
    CATEGORY_CHOICES = [
        ('BLOG', _('Blog')),
        ('NEWS', _('News')),
        ('REVIEW', _('Review')),
        ('TUTORIAL', _('Tutorial')),
    ]
    category = models.CharField(_('Category'), max_length=50, choices=CATEGORY_CHOICES, default='BLOG',blank=True, null=True,
                                help_text=_("Category of the post (e.g., Blog, News)."))

    is_published = models.BooleanField(_('Publication Date'), default=True,
                                       help_text=_(
                                           "Flag indicating whether the post is published."))  # A boolean field to mark if the post is published

    rating = models.DecimalField(_('Rating'), max_digits=3, decimal_places=2, default=0.00,
                                 help_text=_(
                                     "Rating of the post (e.g., a scale from 0 to 5)."))  # A DecimalField for rating or price if the post has any

    website = models.URLField(_('Website'), blank=True, null=True, help_text=_(
        "An external link related to the post."))  # A URL field for an external link or reference

    # A JSON field for storing additional metadata (requires PostgreSQL)
    metadata = models.JSONField(_('Metadata'), blank=True, null=True,
                                help_text=_("Additional metadata related to the post (e.g., JSON structure)."))

    # A field for tags (using Many-to-Many relationship)
    tags = models.ManyToManyField(
        'Tag', blank=True, help_text=_("Tags associated with this post (e.g., #Blog, #lifestyle)."))

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        db_table = "Postify_post"  # Custom table name for the database
        verbose_name = _("Post")  # Singular name for the model
        verbose_name_plural = _("Posts")  # Plural name for the model


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=True, null=True,
                            help_text=_("Tag name to categorize posts."))

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Postify_tag"  # Custom table name for the database
        verbose_name = _("Tag")  # Singular name for the model
        verbose_name_plural = _("Tags")
