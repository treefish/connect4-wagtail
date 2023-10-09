from django.db import models
#from wagtail.admin.panels import FieldPanel


class Partner(models.Model):
    """ A Partner class
        Note: Do all this using the Function approach as per: https://docs.wagtail.org/en/stable/topics/snippets/registering.html
        to get snippet onto admin menu list. Look in wagtail_hooks.py for implementation.
        That makes Partner a simple Django model.
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

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Partner"
        verbose_name_plural = "Partners"
