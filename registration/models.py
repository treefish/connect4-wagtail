from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from datetime import date, datetime

User = get_user_model()


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class FamilyMember(BaseModel):
    family = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="family_member",
    )

    class Types(models.TextChoices):
        PARENT = "PARENT", "Parent / Caregiver"
        CHILD = "CHILD", "Child"

    base_type = Types.PARENT

    # What type of user are we?
    type = models.CharField("Type", max_length=6, choices=Types.choices, default=base_type)

    first_name = models.CharField("First name", max_length=100)
    last_name = models.CharField("Last name", max_length=100)
    diet_req = models.BooleanField("Dietary requirements?", default = False )
    diet_detail = models.TextField("Dietary requirements", max_length=1024, null=True, blank=True)
    medical_req = models.BooleanField("Medical needs?", default = False )
    medical_detail = models.TextField("Medical details", max_length=1024, null=True, blank=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        errors = {}
        if self.diet_req and not self.diet_detail:
            errors["diet_detail"] = "If Dietary Requirements is ticked, Dietary Details must be filled in."

        if self.diet_detail and not self.diet_req:
            errors["diet_req"] = "If dietary information is added, Dietary Requirements must be ticked."

        if self.medical_req and not self.medical_detail:
            errors["medical_detail"] = "If Medical Requirements is ticked, Medical Details must be filled in."

        if self.medical_detail and not self.medical_req:
            errors["medical_req"] = "If medical information is added, Medical Requirements must be ticked."

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return self.full_name


class ParentManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=FamilyMember.Types.PARENT)


class ParentMore(models.Model):
    family_member = models.OneToOneField(FamilyMember, on_delete=models.CASCADE)

    def __str__(self):
        return self.family_member.full_name


class Parent(FamilyMember):
    base_type = FamilyMember.Types.PARENT
    objects = ParentManager()

    @property
    def more(self):
        return self.parentmore

    class Meta:
        proxy = True

    def phrase(self):
        return "Eat your greens!"


class ChildManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=FamilyMember.Types.CHILD)


class ChildMore(models.Model):
    class Gender(models.TextChoices):
        FEMALE = "Female", "Female"
        MALE = "Male", "Male"
        OTHER = "Other", "Other"
        BLANK = "Unanswered", "Prefer not to say"

    base_gender = Gender.BLANK

    class YesNo(models.TextChoices):
        YES = "Yes", "Yes"
        NO = "No", "No"
        BLANK = None, "-"

    base_yesno = YesNo.BLANK

    family_member = models.OneToOneField(FamilyMember, on_delete=models.CASCADE)
    dob = models.DateField('Date of Birth')
    gender = models.CharField('Gender', max_length=10, choices=Gender.choices, default=base_gender)
    school = models.CharField("School", max_length=100, null=True, blank=True)
#    fsm_char = models.CharField("Eligible for benefit related Free School Meals (FSM)?", choices = YesNo.choices, default=base_yesno )
    fsm = models.BooleanField("Eligible for benefit related Free School Meals (FSM)?", null=True)
    sen_req = models.BooleanField("Special educational needs (SEN) or Education health care plan (EHCP)?", null=True)
    sen_req_old = models.CharField("Special educational needs (SEN) or Education health care plan (EHCP)?", choices=YesNo.choices,
                           default=base_yesno)
    sen_detail = models.TextField("SEN Details", max_length=1024, null=True, blank=True)

    @property
    def years_old(self):
        today_datetime = timezone.now()
        today = datetime.date(today_datetime)
        date_diff = relativedelta(today, self.dob)
        return date_diff.years

    # Note: In Master spreadsheet the designations are different from here and Attendance Register Daily
    # Location  < 4          4-10        11-16       >16
    # Master    Toddler      Primary     Secondary
    # Here      Toddler      Child       Teenager    Post-Teen
    # Daily     < 4          4-10        Teenager
    # For next clean up, will look to harmonise terminology.

    '''
    Dates
    today_datetime = timezone.now()
    today = datetime.date(today_datetime)
    dob > today
    '''

    @property
    def is_teenager(self):
        return self.years_old in range(11, 17)  # 11-16

    @property
    def is_secondary(self):
        # Same as 'teenager', 'secondary' is used in reports.
        return self.years_old in range(11, 17) # 11-16

    @property
    def is_child(self):
        # This definition of child is a Child between 4 and 10 (as required by reports)
        return self.years_old in range(4, 11)

    @property
    def is_primary(self):
        # Same as 'child', 'primary' is used in reports.
        return self.years_old in range(4, 11)

    @property
    def is_toddler(self):
        return self.years_old < 4

    @property
    def is_post_teen(self):
        # Funding is only up to 16, so this will show how many are set as Child but over 16.
        return self.years_old > 16

    @property
    def is_time_traveller(self):
        # DoB is in the future!
        today_datetime = timezone.now()
        today = datetime.date(today_datetime)
        return self.dob > today if self.dob else False

    @property
    def is_too_old(self):
        # DoB makes them older than 25! Become an Adult (Parent)!
        return self.years_old > 25

    @property
    def is_immortal(self):
        # DoB makes them older than 100!
        return self.years_old > 99

    def clean(self):
        errors = {}

        if self.sen_req == None: #self.base_yesno:
                errors["sen_req"] = "SEN/EHCP must be explicitly answered as 'Yes' or 'No'"
        elif not self.sen_detail and self.sen_req:
            errors["sen_detail"] = "If SEN Requirements is 'Yes'', SEN details must be filled in."

        if self.sen_detail and not self.sen_req:
            errors["sen_req"] = "If SEN details are filled in, SEN Requirements must be ticked."

        if self.dob and self.is_time_traveller:
            errors["dob"] = "Date of Birth is in the future. A time traveller?"

        if self.dob and self.is_post_teen:
            if self.is_immortal:
                errors[
                    "dob"] = "Date of Birth makes this Child nigh immortal. Please check your date."
            elif self.is_too_old:
                errors[
                    "dob"] = "Date of Birth makes this Child an adult. Please add this person as a parent (adult)"
            else:
                errors["dob"] = "Date of Birth makes this Child too old to be considered as such. Please add this person as a parent (adult)"

        print(f"* Checking FSM: {self.fsm}")
        if self.fsm == None:
                errors["fsm"] = "FSM must be explicitly answered as 'Yes' or 'No'"

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.dob} - {self.gender} - {self.fsm}"

'''
>>> child = Child.objects.get(id=2)
SELECT "registration_familymember"."id",
       "registration_familymember"."created_at",
       "registration_familymember"."updated_at",
       "registration_familymember"."family_id",
       "registration_familymember"."type",
       "registration_familymember"."first_name",
       "registration_familymember"."last_name",
       "registration_familymember"."diet_req",
       "registration_familymember"."diet_detail",
       "registration_familymember"."medical_req",
       "registration_familymember"."medical_detail"
  FROM "registration_familymember"
 WHERE ("registration_familymember"."type" = 'CHILD' AND "registration_familymember"."id" = 2)
 LIMIT 21
Execution time: 0.001513s [Database: default]
>>> child
<Child: Junior Deimos>
>>> child.childmore.dob
SELECT "registration_childmore"."id",
       "registration_childmore"."family_member_id",
       "registration_childmore"."dob",
       "registration_childmore"."gender",
       "registration_childmore"."school",
       "registration_childmore"."fsm",
       "registration_childmore"."sen_req",
       "registration_childmore"."sen_detail"
  FROM "registration_childmore"
 WHERE "registration_childmore"."family_member_id" = 2
 LIMIT 21
Execution time: 0.001186s [Database: default]
datetime.date(2013, 10, 11)
>>> child.childmore.years_old
10
>>> child.childmore.is_teenager
False
>>> child.childmore.is_child
True
>>> child.childmore.is_toddler
False
>>> child.childmore.is_post_teen
False
>>> child.childmore.is_time_traveller
False
>>> child.childmore.is_immortal
False
>>> child.childmore.is_too_old
False
'''

class Child(FamilyMember):
    base_type = FamilyMember.Types.CHILD
    objects = ChildManager()

    @property
    def more(self):
        return self.childmore

    class Meta:
        proxy = True
        verbose_name_plural = "Children"

    def phrase(self):
        return "I'm not tired!"
