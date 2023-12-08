from wagtail import hooks

from .views import parent_viewset, child_viewset


@hooks.register("register_admin_viewset")
def register_parent_viewset():
    return parent_viewset

@hooks.register("register_admin_viewset")
def register_child_viewset():
    return child_viewset