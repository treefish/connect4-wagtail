from django.urls import path
from . import views

urlpatterns = [
    path("", views.EventListView.as_view(), name="events"),
    path("event/<int:pk>/detail/", views.EventDetailView.as_view(), name="event_detail"),
    path("event/<int:pk>/bookings/", views.EventBookingsListView.as_view(), name="event_bookings_list"),
    # path('event/create/', views.EventCreateView.as_view(), name='event_create'),
    # path('event/<int:pk>/update/', views.EventUpdateView.as_view(), name='event_update'),
    # path('event/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
    #
    # path("event/<int:pk>/attendance_list/", views.EventAttendanceView.as_view(), name="event_attendance_list"),
    # path("event/<int:pk>/bookings/", views.EventBookingsView.as_view(), name="event_bookings_list"),
    # path("event/<int:pk>/upload_wp_attendance_register/", views.UploadWPAttendanceRegister.as_view(),
    #      name="upload_wp_attendance_register"),
    # path("event/<int:pk>/upload_attendance_register_daily/", views.UploadAttendanceRegisterDaily.as_view(),
    #      name="upload_attendance_register_daily"),
    # path("event/<int:pk>/download_attendance_register_daily/", views.DownloadAttendanceRegisterDaily.as_view(),
    #      name="download_attendance_register_daily"),
    #
    # path("projects", views.ProjectListView.as_view(), name="projects"),
    # path("project/<int:pk>/detail/", views.ProjectDetailView.as_view(),
    #      name="project_detail"),
    # path("project/<int:pk>/attendance_summary/", views.ProjectSummaryView.as_view(),
    #      name="project_attendance_summary"),
    # path("project/<int:pk>/upload_attendance_register/", views.UploadAttendanceRegister.as_view(),
    #      name="upload_attendance_register"),
    # path("project/<int:pk>/download_attendance_register/", views.DownloadAttendanceRegister.as_view(),
    #      name="download_attendance_register"),
    # path("project/<int:pk>/download_master_weekly_monitoring_statement/", views.DownloadMasterWeeklyMonitoringStatement.as_view(),
    #      name="download_master_weekly_monitoring_statement"),
    # path("project/<int:pk>/unique_attendees_list/", views.ProjectUniqueAttendeesView.as_view(),
    #      name="project_unique_attendees_list"),
    # path("project/<int:pk>/download_attendance_register_unique/", views.DownloadAttendanceRegisterUnique.as_view(),
    #      name="download_attendance_register_unique"),
]
