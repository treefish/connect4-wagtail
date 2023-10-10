from django.urls import path
from .views import profile_view, CustomUserDeleteView, CustomUserUpdateView

urlpatterns = [
    path('profile/', profile_view, name='account_profile'),
    path('profile/update/', CustomUserUpdateView.as_view(template_name='account/update.html'), name='account_update'),
#    path('profile/<int:pk>/update/', CustomUserUpdateView.as_view(template_name='account/update.html'), name='account_update'),

#    path('<int:pk>/delete/', CustomUserDeleteView.as_view(template_name='account/delete.html'), name='account_delete'),
]