from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, MultiWidgetField
from crispy_forms.bootstrap import InlineRadios
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
        help_texts = {'diet_req': "Confirm by ticking if this family member has dietary considerations.",
                      'diet_detail': "If Dietary Requirements is ticked, describe these here.",
                      'medical_req': "Confirm by ticking if this family member has medical considerations.",
                      'medical_detail': "If Medical Requirements is ticked, describe these here."
                      }


# ChildMore fields
class FamilyMemberChildForm(forms.ModelForm):
#     fsm = forms.TypedChoiceField(
#         label="Free School Meal?",
#         choices=((1, "Yes"), (0, "No")),
#         coerce=lambda x: bool(int(x)),
#         widget=forms.RadioSelect,
# #        initial='1',
#         required=True,
#     )

    class Meta:
        model = ChildMore
        fields = (
            'dob',
            'gender',
            'school',
            'fsm',
            'sen_req', 'sen_detail',
        )
# this works...        widgets = {'dob': forms.SelectDateWidget(years=range(timezone.now().year - 25, timezone.now().year + 1))}
        BOOLEAN_CHOICES = ((True, 'Yes'), (False, 'No'))
        widgets = {'dob': forms.widgets.DateInput(attrs={'type': 'date'}),
#                   'fsm': forms.widgets.NullBooleanSelect()
                   }
        help_texts = {'fsm': "FSM must be explicitly answered as 'Yes' or 'No'",
                      'sen_req': "SEN/EHCP must be explicitly answered as 'Yes' or 'No'",
                      'sen_detail': "Describe SEN and/or EHCP details here."}

        # https://stackoverflow.com/questions/3468814/python-django-booleanfield-model-with-radioselect-form-default-to-empty


        # widgets = {'fsm': forms.TypedChoiceField(
        # label = "Eligible for benefit related Free School Meals (FSM)?????",
        # choices = ((1, "Yes"), (0, "No"), (None, "-")),
        # coerce = lambda x: bool(int(x)),
        # widget = forms.RadioSelect,
        # initial = None,
        # required = True,
        # ) }

                       #forms.BooleanField(widget=forms.RadioSelect(choices=FamilyMemberChildForm.choices))}

    def __init__(self, *args, **kwargs):
        super(FamilyMemberChildForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

#        BOOLEAN_CHOICES = (('1', 'Yes'), ('0', 'No'))
        # Filtering fields
       #self.fields['fsm'] = forms.ChoiceField(
        # widgets = {'fsm': forms.ChoiceField(
        #     label="FSM label",
        #     # uses items in BOOLEAN_CHOICES
        #     choices=BOOLEAN_CHOICES,
        #     widget=forms.RadioSelect
        #     )
        # }


        # self.helper.layout = Layout(
        #         MultiWidgetField('dob', attrs=({'style': 'width: 33%; display: inline-block;'})),
        #         'gender',
        #
        #         InlineRadios('fsm'),
        #         'sen_req',
        #         'sen_detail',
        #         'school',
        #     )




        # choices = ((1, "Yes"), (0, "No"))
        # self.fields['fsm'].widget = forms.RadioSelect(choices=choices)
        # self.fields['fsm'].required = True


    #     BinaryFieldsList = ['fsm', 'sen_req']
    #     for field in BinaryFieldsList:
    #         self.fields[field].widget = forms.RadioSelect(choices=FamilyMemberChildForm.choices)
