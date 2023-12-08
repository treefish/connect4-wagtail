#from django.views.generic import TemplateView
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
#from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.edit import FormView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from events.models import ProjectPage, EventPage, EventType
from bookings.models import Booking, Attendance
from django.db.models import Count

# For Function based views
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from .forms import UploadAttendanceRegisterForm
from .utils import (
    create_attendance_register_daily,
    import_attendance_register_daily
)

def is_member(user):
    # Used to restrict access to sensitive pages.
    return user.is_superuser or user.groups.filter(name='Editors').exists()


### Events
class EventBaseView(LoginRequiredMixin, UserPassesTestMixin, View):
    model = EventPage
    fields = '__all__'
    success_url = reverse_lazy('eventadmin:events')

    def test_func(self):
        return is_member(self.request.user)


class EventListView(EventBaseView, ListView):
    """View to list all events.
     Use the 'eventpage_list' variable in the template
     to access all Event objects"""

    template_name = 'eventadmin/event_list.html'


class EventDetailView(EventBaseView, DetailView):
    """View to list the details from one event.
    Use the 'event' variable in the template to access
    the specific event here and in the Views below"""

    template_name = 'eventadmin/event_detail.html'


class EventBookingsListView(EventBaseView, DetailView):
    """View to list the details from one event.
    Use the 'event' variable in the template to access
    the specific event here and in the Views below"""

    template_name = 'eventadmin/event_bookings_list.html'


########################################################################################################################
# Reporting
# These functions/classes are taken from connect4-django app
########################################################################################################################

class EventAttendanceView(EventBaseView, DetailView):
    template_name = 'eventadmin/event_attendance_list.html'
    paginate_by = 50


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_id = self.kwargs['pk']
        print(f"Event ID: {event_id}")
        stats = {}

        attendance_list = Attendance.objects.select_related('family_member').filter(booking__event=event_id).select_related('family_member__childmore')
        stats['registered_total'] = attendance_list.count()

        parents_list = attendance_list.filter(family_member__type='PARENT')
        stats['parents_attended_total'] = parents_list.filter(attended=True).count()
        stats['parents_not_attended_total'] = parents_list.filter(attended=False).count()
        stats['parents_total'] = stats['parents_attended_total'] + stats['parents_not_attended_total']

        children_list = attendance_list.filter(family_member__type='CHILD')
        children_attended_list = children_list.filter(attended=True)
        children_not_attended_list = children_list.filter(attended=False)

        # Child (< 4>) Toddler / Youngster
        ids = [attendance.id for attendance in children_attended_list if attendance.family_member.childmore.is_toddler]
        stats['children_lt_4_attended_total'] = children_attended_list.filter(id__in=ids).count()
        ids = [attendance.id for attendance in children_not_attended_list if attendance.family_member.childmore.is_toddler]
        stats['children_lt_4_not_attended_total'] = children_not_attended_list.filter(id__in=ids).count()
        stats['children_lt_4_total'] = stats['children_lt_4_attended_total'] + stats['children_lt_4_not_attended_total']

        # Child (4-10) Primary
        ids = [attendance.id for attendance in children_attended_list if attendance.family_member.childmore.is_child]
        stats['children_4_10_attended_total'] = children_attended_list.filter(id__in=ids).count()
        ids = [attendance.id for attendance in children_not_attended_list if attendance.family_member.childmore.is_child]
        stats['children_4_10_not_attended_total'] = children_not_attended_list.filter(id__in=ids).count()
        stats['children_4_10_total'] = stats['children_4_10_attended_total'] + stats['children_4_10_not_attended_total']

        # Child (11-16) Secondary / Teenager
        ids = [attendance.id for attendance in children_attended_list if attendance.family_member.childmore.is_teenager]
        stats['teens_attended_total'] = children_attended_list.filter(id__in=ids).count()
        ids = [attendance.id for attendance in children_not_attended_list if attendance.family_member.childmore.is_teenager]
        stats['teens_not_attended_total'] = children_not_attended_list.filter(id__in=ids).count()
        stats['teens_total'] = stats['teens_attended_total'] + stats['teens_not_attended_total']

        # Child (> 16) Post-teen
        ids = [attendance.id for attendance in children_attended_list if attendance.family_member.childmore.is_post_teen]
        stats['post_teens_attended_total'] = children_attended_list.filter(id__in=ids).count()
        ids = [attendance.id for attendance in children_not_attended_list if attendance.family_member.childmore.is_post_teen]
        stats['post_teens_not_attended_total'] = children_not_attended_list.filter(id__in=ids).count()
        stats['post_teens_total'] = stats['post_teens_attended_total'] + stats['post_teens_not_attended_total']

        stats['attended_total'] = stats['parents_attended_total'] \
                                + stats['children_lt_4_attended_total'] \
                                + stats['children_4_10_attended_total'] \
                                + stats['teens_attended_total'] \
                                + stats['post_teens_attended_total']

        stats['not_attended_total'] = stats['parents_not_attended_total'] \
                                + stats['children_lt_4_not_attended_total'] \
                                + stats['children_4_10_not_attended_total'] \
                                + stats['teens_not_attended_total'] \
                                + stats['post_teens_not_attended_total']

        # Children 4-10 Attended, FSM, SEN
        ids = [attendance.id for attendance in children_attended_list if (attendance.family_member.childmore.is_child and attendance.family_member.childmore.fsm and attendance.family_member.childmore.sen_req)]
        print(f"ids: {len(ids)}\tChildren 4-10 Attended, FSM, SEN")
        stats['children_4_10_attended_fsm_sen_total'] = children_attended_list.filter(id__in=ids).count()

        # Children 4-10 Attended, FSM, Non-SEN
        ids = [attendance.id for attendance in children_attended_list if (attendance.family_member.childmore.is_child and attendance.family_member.childmore.fsm and not attendance.family_member.childmore.sen_req)]
        print(f"ids: {len(ids)}\tChildren 4-10 Attended, FSM, non-SEN")
        stats['children_4_10_attended_fsm_non_sen_total'] = children_attended_list.filter(id__in=ids).count()

        # Children 4-10 Attended, non-FSM, SEN
        ids = [attendance.id for attendance in children_attended_list if (
                    attendance.family_member.childmore.is_child and not attendance.family_member.childmore.fsm and attendance.family_member.childmore.sen_req)]
        print(f"ids: {len(ids)}\tChildren 4-10 Attended, non-FSM, SEN")
        stats['children_4_10_attended_non_fsm_sen_total'] = children_attended_list.filter(id__in=ids).count()

        # Children 4-10 Attended, non-FSM, Non-SEN
        ids = [attendance.id for attendance in children_attended_list if (
                    attendance.family_member.childmore.is_child and not attendance.family_member.childmore.fsm and not attendance.family_member.childmore.sen_req)]
        print(f"ids: {len(ids)}\tChildren 4-10 Attended, non-FSM, non-SEN")
        stats['children_4_10_attended_non_fsm_non_sen_total'] = children_attended_list.filter(id__in=ids).count()

        # Teenager Attended, FSM, SEN
        ids = [attendance.id for attendance in children_attended_list if (attendance.family_member.childmore.is_teenager and attendance.family_member.childmore.fsm and attendance.family_member.childmore.sen_req)]
        print(f"ids: {len(ids)}\tTeenager Attended, FSM, SEN")
        stats['teens_attended_fsm_sen_total'] = children_attended_list.filter(id__in=ids).count()

        # Teenager Attended, FSM, Non-SEN
        ids = [attendance.id for attendance in children_attended_list if (attendance.family_member.childmore.is_teenager and attendance.family_member.childmore.fsm and not attendance.family_member.childmore.sen_req)]
        print(f"ids: {len(ids)}\tTeenager Attended, FSM, non-SEN")
        stats['teens_attended_fsm_non_sen_total'] = children_attended_list.filter(id__in=ids).count()

        # Teenager Attended, non-FSM, SEN
        ids = [attendance.id for attendance in children_attended_list if (
                    attendance.family_member.childmore.is_teenager and not attendance.family_member.childmore.fsm and attendance.family_member.childmore.sen_req)]
        print(f"ids: {len(ids)}\tTeenager Attended, non-FSM, SEN")
        stats['teens_attended_non_fsm_sen_total'] = children_attended_list.filter(id__in=ids).count()

        # Teenager Attended, non-FSM, Non-SEN
        ids = [attendance.id for attendance in children_attended_list if (
                    attendance.family_member.childmore.is_teenager and not attendance.family_member.childmore.fsm and not attendance.family_member.childmore.sen_req)]
        print(f"ids: {len(ids)}\tTeenager Attended, non-FSM, non-SEN")
        stats['teens_attended_non_fsm_non_sen_total'] = children_attended_list.filter(id__in=ids).count()

        context['stats'] = stats
        context['attendance_list'] = attendance_list
        print(f"Stats: {stats}")
        return context


class DownloadAttendanceRegisterDaily(EventBaseView, DetailView):
    template_name = 'eventadmin/download_attendance_register.html'

    def get(self, request, *args, **kwargs):
        event = super().get_object()
        filename = f"Attendance Register Daily - {event.title}.xlsx"
        create_attendance_register_daily(event, filename)
        success_url = f"/media/admin/{filename}"
        return redirect(success_url)


class UploadAttendanceRegisterDaily(EventBaseView, FormView):
    '''
    Upload a pre-generated Attendance Register Daily and updates the Booking & Attendance entries for the event
    found in the spreadsheet.
    Refer:
    https://docs.djangoproject.com/en/4.2/ref/files/uploads
    https://www.andygoldschmidt.com/2014/09/10/django-file-uploads-with-class-based-views/

    Note: This will need to be modified to use Celery as it takes a while to process the spreadsheet. Using Celery to
    offload the processing will return the page back to the user much more quickly.
    Can also then use something like a Progress Bar to keep the user updated on progress.
    Refer:
    https://www.freecodecamp.org/news/how-to-build-a-progress-bar-for-the-web-with-django-and-celery-12a405637440/
    '''
    template_name = "eventadmin/upload_attendance_register_daily.html"
    # Might be able to use the same form as WP AR
    form_class = UploadAttendanceRegisterForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            context = super().get_context_data(**kwargs)
            event_id = self.kwargs['pk']
            print(f"Handling the FORM for event {event_id}!")
            file = request.FILES["file"]
            print(f"Uploaded: {file.name} - Type: {file.content_type}")  # {file.temporary_file_path}")

            # Let's check the file type at least.
            if file.content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                # Save to disk so it can be read by Openpyxl
                with open(f"media/admin/{file.name}", "wb+") as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)

                # Process the uploaded Attendance Register spreadsheet into Booking and Attendance entries.
                # Note: The events in the spreadsheet will have event_id associated, so
                # it doesn't actually matter if the spreadsheet is for this project or not.
                import_attendance_register_daily(f"media/admin/{file.name}", event_id)
            else:
                print(f"Incorrect file type for uploaded Attendance Register! Type is '{file.content_type}'")
            success_url = reverse_lazy('event_detail', kwargs = {'pk': event_id})
            return redirect(success_url)
        else:
            return render(request, self.template_name, {'form': form})



### Projects
class ProjectBaseView(LoginRequiredMixin, UserPassesTestMixin, View):
    model = ProjectPage
    fields = '__all__'
    success_url = reverse_lazy('projects')


    def test_func(self):
        return is_member(self.request.user)


class ProjectListView(ProjectBaseView, ListView):
    """View to list all projects.
     Use the 'project_list' variable in the template
     to access all Project objects"""

    template_name = 'eventadmin/project_list.html'


class ProjectDetailView(ProjectBaseView, DetailView):
    """View to list the details from one project.
    Use the 'project' variable in the template to access
    the specific project here and in the Views below"""

    template_name = 'eventadmin/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs['pk']
        project = ProjectPage.objects.get(id=project_id)

        event_list = EventPage.objects.live().descendant_of(project).order_by("-start_date")
            #EventPage.objects.filter(project=project_id).order_by("-start_date")
        context['event_list'] = event_list
        return context


class ProjectSummaryView(ProjectBaseView, DetailView):
    """View to list the details from one project.
    Use the 'project' variable in the template to access
    the specific project here and in the Views below"""

    template_name = 'eventadmin/project_summary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs['pk']
        project = ProjectPage.objects.get(id=project_id)
        # print(f"Project ID: {project_id}")
        stats = []

        event_list = EventPage.objects.live().descendant_of(project).order_by("start_date")
        # get a list of unique weeks for the Events in this Project. 'weeks' is a list or at least is iterable.
        weeks = event_list.order_by().values_list('week', flat=True).distinct().order_by("week")
        for week in weeks:
            week_events = event_list.filter(week=week)
            week_attendance_list = Attendance.objects.filter(booking__event__in=week_events)
            #
            parents_registered = week_attendance_list.filter(family_member__type='PARENT')
            parents_attended = parents_registered.filter(attended=True)
            parents_attended_unique = parents_attended.values("family_member").annotate(attendances=Count('family_member'))\
                .order_by('family_member__last_name', 'family_member__first_name')
            children_registered = week_attendance_list.filter(family_member__type='CHILD')
            children_attended = children_registered.filter(attended=True)
            children_attended_unique = children_attended.values("family_member").annotate(attendances=Count('family_member'))\
                .order_by('family_member__last_name', 'family_member__first_name')

            print(f"Week: {week} - PAT: {parents_attended.count()}\tUnique: {parents_attended_unique.count()}\tPAT: {children_attended.count()}\tUnique: {children_attended_unique.count()}")
            week_stats = {'week_number': week,
                          'parents_registered': parents_registered.count(),
                          'parents_attended': parents_attended.count(),
                          'parents_attended_unique': parents_attended_unique.count(),
                          'children_registered': children_registered.count(),
                          'children_attended': children_attended.count(),
                          'children_attended_unique': children_attended_unique.count(),
                          }
            stats.append(week_stats)

        context['stats'] = stats
        print(f"Stats: {stats}")
        return context


class ProjectUniqueAttendeesView(ProjectBaseView, DetailView):
    """View to list the Attendees and how many events they have attended.
    Use the 'project' variable in the template to access
    the specific project here and in the Views below"""

    template_name = 'eventadmin/project_unique_attendees_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs['pk']
        project = ProjectPage.objects.get(id=project_id)
        print(f"Project ID: {project_id}")

        event_type = EventType.objects.get(name="Family Fun Days")
        #event_list = Event.objects.filter(project=project_id, event_type=event_type)  # Family Fun Day events only
        event_list = EventPage.objects.live().descendant_of(project).filter(event_type=event_type).order_by("start_date")
        event_count = event_list.count()

        all_registered = Attendance.objects.filter(booking__event__in=event_list)
        children_registered = all_registered.filter(family_member__type="CHILD").select_related(
            "family_member__childmore")
        children_attended = children_registered.filter(attended=True).select_related("family_member__childmore").order_by("family_member__last_name", "family_member__first_name")
#        children_attended_unique = children_attended.distinct("family_member__last_name", "family_member__first_name")#.order_by("family_member__last_name", "family_member__first_name")
        children_attended_unique = children_attended.values("family_member").annotate(num=Count("family_member")).values_list("family_member__first_name", "family_member__last_name", "num")

        print(f"Registered: {all_registered.count()}\tChildren registered: {children_registered.count()}\tChildren attended: {children_attended.count()}")
        # for cau in children_attended_unique:
        #     print(F" - {cau}")
        context['attendance_list'] = children_attended_unique

        # context['bookings'] = Booking.objects.filter(family__registrant=self.request.user)
        # context['family'] = Family.objects.get(registrant=self.request.user)
        return context

