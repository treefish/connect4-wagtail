from django import forms
from django.contrib.auth import get_user_model
from .models import FamilyMember, ChildMore

User = get_user_model()


# FamilyMember (Parent and Child)
class FamilyMemberForm(forms.ModelForm):
    class Meta:
        model = FamilyMember
        fields = (
            'type',
            'first_name',
            'last_name',
            'diet_req', 'diet_detail',
            'medical_req', 'medical_detail',
        )
        widgets = {'type': forms.HiddenInput()}


# ChildMore fields
class FamilyMemberChildForm(forms.ModelForm):
    class Meta:
        model = ChildMore
        fields = (
            'dob',
            'gender',
            'school',
            'fsm',
            'sen_req',
            'sen_detail',
        )

