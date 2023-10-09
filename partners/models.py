from django.db import models

from wagtail.snippets.models import register_snippet

@register_snippet
class Partner(models.Model):
    """ A Partner class
    """

    name = models.TextField(max_length=100, blank=False, null=False)
    url = models.URLField(null=True, blank=True)
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        help_text="This image should be the partner logo and will be cropped to a maximum of ?px by ?px on the Partner page.",
        related_name="+",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("url"),
        FieldPanel("logo"),
    ]

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Partner"
        verbose_name_plural = "Partners"
