from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from dateutil.relativedelta import relativedelta
from datetime import *

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
        FEMALE = "FEMALE", "Female"
        MALE = "MALE", "Male"
        OTHER = "OTHER", "Other"
        BLANK = "BLANK", "-"

    base_gender = Gender.BLANK

    family_member = models.OneToOneField(FamilyMember, on_delete=models.CASCADE)
    dob = models.DateField('Date of Birth')
    gender = models.CharField('Gender', max_length=6, choices=Gender.choices, default=base_gender)
    school = models.TextField("School", max_length=100, null=True, blank=True)
    fsm = models.BooleanField("Free School Meal?", default = False )
    sen_req = models.BooleanField("SEN Requirements?", default = False )
    sen_detail = models.TextField("SEN Requirements", max_length=1024, null=True, blank=True)

    @property
    def years_old(self):
        date_diff = relativedelta(datetime.today(), self.dob)
        return date_diff.years

    # Note: In Master spreadsheet the designations are different from here and Attendance Register Daily
    # Location  < 4          4-10        11-16       >16
    # Master    Toddler      Primary     Secondary
    # Here      Youngster    Child       Teenager    Post-Teen
    # Daily     < 4          4-10        Teenager
    # For next clean up, will look to harmonise terminology.

    @property
    def is_teenager(self):
        teenager = self.years_old in range(11, 17) # 11-16
        return teenager

    @property
    def is_child(self):
        # This definition of child is a Child between 4 and 10 (as required by reports)
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
        return self.dob > datetime.now().date()

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
        if self.sen_req and not self.sen_detail:
            errors["sen_detail"] = "If SEN Requirements is ticked, SEN Details must be filled in."

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.dob} - {self.gender} - {self.fsm}"


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
