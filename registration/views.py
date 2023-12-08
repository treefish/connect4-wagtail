from django.http.response import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from .models import FamilyMember
from .forms import FamilyMemberForm, FamilyMemberChildForm

User = get_user_model()

def create_family_member(request):
    user = User.objects.get(id=request.user.id)
    family_members = FamilyMember.objects.filter(family=user)
    form = FamilyMemberForm(request.POST or None)
    child_form = FamilyMemberChildForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            family_member = form.save(commit=False)
            family_member.family = user
            if family_member.type == FamilyMember.Types.PARENT:
                print("* Processing PARENT form")
                family_member.save()
                return redirect("detail-family-member", pk=family_member.id)
            elif family_member.type == FamilyMember.Types.CHILD:
                if child_form.is_valid():
                    family_member.type = FamilyMember.Types.CHILD
                    family_member.save()
                    childmore = child_form.save(commit=False)
                    childmore.family_member = family_member

                    childmore.save()

                    return redirect("detail-family-member", pk=family_member.id)
                else:
                    return render(request, "registration/partials/family_member_form.html", context={
                        "form": form,
                        "child_form": child_form,
                    })
        else:
            return render(request, "registration/partials/family_member_form.html", context={
                "form": form,
                "child_form": child_form,
            })

    context = {
        "form": form,
        "child_form": child_form,
        "user": user,
        "family_members": family_members
    }

    return render(request, "registration/create_family_member.html", context)


def create_family_member_form(request):
    form = FamilyMemberForm(initial = {'type': FamilyMember.Types.PARENT})
    context = {
        "form": form
    }
    return render(request, "registration/partials/family_member_form.html", context)


def create_family_member_child_form(request):
    form = FamilyMemberForm(initial={'type': FamilyMember.Types.CHILD})
    child_form = FamilyMemberChildForm() #initial={'fsm': None})
    context = {
        "form": form,
        "child_form": child_form
    }
    return render(request, "registration/partials/family_member_child_form.html", context)


def detail_family_member(request, pk):
    family_member = get_object_or_404(FamilyMember, id=pk)
    context = {
        "family_member": family_member
    }
    return render(request, "registration/partials/family_member_detail.html", context)


def update_family_member(request, pk):
    family_member = FamilyMember.objects.get(id=pk)

    form = FamilyMemberForm(request.POST or None, instance=family_member)
    if family_member.type == FamilyMember.Types.CHILD:
        childmore = family_member.childmore
        child_form = FamilyMemberChildForm(request.POST or None, instance=childmore)
    else:
        child_form = FamilyMemberForm(None)

    if request.method == "POST":
        if form.is_valid():
            family_member = form.save(commit=False)
            if family_member.type == FamilyMember.Types.PARENT:
                family_member.save()
                return redirect("detail-family-member", pk=family_member.id)
            elif family_member.type == FamilyMember.Types.CHILD:
                if child_form.is_valid():
                    family_member.type = FamilyMember.Types.CHILD
                    family_member.save()
                    childmore = child_form.save(commit=False)
                    childmore.family_member = family_member
                    childmore.save()

                    return redirect("detail-family-member", pk=family_member.id)
                else:
                    return render(request, "registration/partials/family_member_form.html", context={
                        "form": form,
                        "child_form": child_form,
                        "family_member": family_member
                    })
        else:
            return render(request, "registration/partials/family_member_form.html", context={
                "form": form,
                "child_form": child_form,
                "family_member": family_member
            })

    context = {
        "form": form,
        "child_form": child_form,
        "family_member": family_member
    }

    return render(request, "registration/partials/family_member_form.html", context)


# No removal of Family members allowed at this stage.
# Ref: Video meeting with Flo, 26 Oct 2023
# def delete_family_member(request, pk):
#     family_member = get_object_or_404(FamilyMember, id=pk)
#
#     if request.method == "POST":
#         family_member.delete()
#         return HttpResponse("")
#
#     return HttpResponseNotAllowed(
#         [
#             "POST",
#         ]
#     )


# https://docs.wagtail.org/en/stable/extending/generic_views.html
# Check wagtail_hooks.py for more

from wagtail.admin.viewsets.model import ModelViewSet
from .models import Parent, Child

class ParentViewSet(ModelViewSet):
    model = Parent
    form_fields = ["first_name", "last_name", "diet_req", "diet_detail", "medical_req", "medical_detail"]
    list_display = ["first_name", "last_name", "diet_req", "medical_req"]
    icon = "user"
    add_to_admin_menu = False
    add_to_settings_menu = True
    inspect_view_enabled = True


parent_viewset = ParentViewSet("parent")  # defines /admin/parent/ as the base URL


class ChildViewSet(ModelViewSet):
    model = Child
    form_fields = ["first_name", "last_name", "diet_req", "diet_detail", "medical_req", "medical_detail"]
    list_display = ["first_name", "last_name", "diet_req", "medical_req"]
    icon = "user"
    add_to_admin_menu = False
    add_to_settings_menu = True
    inspect_view_enabled = True


child_viewset = ChildViewSet("child")  # defines /admin/child/ as the base URL