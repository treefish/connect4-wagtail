# # partners/wagtail_hooks.py
# from wagtail.snippets.models import register_snippet
# from wagtail.snippets.views.snippets import SnippetViewSet
# from wagtail.admin.panels import FieldPanel
#
# from partners.models import Partner
#
# class PartnerViewSet(SnippetViewSet):
#     model = Partner
#     icon = "placeholder"
#     menu_label = "Partners"
#     menu_name = "partners"
#     menu_order = 300
#     add_to_admin_menu = True
#
#     panels = [
#         FieldPanel("name"),
#         FieldPanel("url"),
#         FieldPanel("logo"),
#     ]
#
# # Instead of using @register_snippet as a decorator on the model class,
# # register the snippet using register_snippet as a function and pass in
# # the custom SnippetViewSet subclass.
#
# register_snippet(PartnerViewSet)