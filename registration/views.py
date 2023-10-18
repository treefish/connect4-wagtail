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
                print("* Processing CHILD form")
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
    child_form = FamilyMemberChildForm
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
                print("* Processing PARENT form")
                family_member.save()

                return redirect("detail-family-member", pk=family_member.id)
            elif family_member.type == FamilyMember.Types.CHILD:
                print("* Processing CHILD form")
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
        "family_member": family_member
    }

    return render(request, "registration/partials/family_member_form.html", context)


def delete_family_member(request, pk):
    family_member = get_object_or_404(FamilyMember, id=pk)

    if request.method == "POST":
        family_member.delete()
        return HttpResponse("")

    return HttpResponseNotAllowed(
        [
            "POST",
        ]
    )

