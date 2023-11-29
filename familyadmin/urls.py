from django.urls import path
from . import views

urlpatterns = [
    path("", views.FamilyListView.as_view(), name="family_list"),
    path("<int:pk>", views.FamilyDetailView.as_view(), name="family_detail"),
#    path("<str:upn>/print", views.FamilyPrintView.as_view(), name="family_print"),

]
