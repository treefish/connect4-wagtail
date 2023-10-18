from django.contrib import admin
from django.urls import path

from bookings.views import BookingsListView, create_booking, create_booking_form, detail_booking, update_booking_attendees, delete_booking

urlpatterns = [
    path('', create_booking, name='bookings'),
    path('htmx/create-booking-form/', create_booking_form, name='create-booking-form'),
    path('htmx/booking/<pk>/', detail_booking, name="detail-booking"),
    path('htmx/booking/<pk>/update/', update_booking_attendees, name="update-booking-attendees"),
    path('htmx/booking/<pk>/delete/', delete_booking, name="delete-booking"),

]