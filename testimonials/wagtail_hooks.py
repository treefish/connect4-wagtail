# partners/wagtail_hooks.py
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.admin.panels import FieldPanel

from testimonials.models import Testimonial

class TestimonialViewSet(SnippetViewSet):
    model = Testimonial
    icon = "placeholder"
    menu_label = "Testimonials"
    menu_name = "testimonials"
    menu_order = 300
    add_to_admin_menu = True

    panels = [
        FieldPanel("quote"),
        FieldPanel("attribution"),
    ]

# Instead of using @register_snippet as a decorator on the model class,
# register the snippet using register_snippet as a function and pass in
# the custom SnippetViewSet subclass.

register_snippet(TestimonialViewSet)