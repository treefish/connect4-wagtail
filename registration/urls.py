from django.contrib import admin
from django.urls import path

from registration.views import create_family_member, create_family_member_form, detail_family_member, update_family_member\
#    , delete_family_member
from registration.views import create_family_member_child_form

urlpatterns = [
#    path('<pk>/', create_family_member, name='create-family-member'),
    path('family_members/', create_family_member, name='family-members'),
    path('htmx/create-family-member-form/', create_family_member_form, name='create-family-member-form'),
    path('htmx/create-family-member-child-form/', create_family_member_child_form,
         name='create-family-member-child-form'),
    path('htmx/family_member/<pk>/', detail_family_member, name="detail-family-member"),
    path('htmx/family_member/<pk>/update/', update_family_member, name="update-family-member"),
# No removal of Family members allowed at this stage.
#    path('htmx/family_member/<pk>/delete/', delete_family_member, name="delete-family-member"),


]