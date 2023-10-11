from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from dateutil.relativedelta import relativedelta
from datetime import *
# # For generating unique wp_member_id in FamilyMember where one is created manually, rather than through sync from Wordpress.
# import random
# import string
# import uuid

# class WPUsermeta(models.Model):
#     user_id = models.PositiveIntegerField("User ID")
#     meta_key = models.CharField("Meta Key", max_length=50)
#     meta_value = models.TextField("Meta Value")
#
#     class Meta:
#         ordering = ['user_id', 'meta_key']
#         verbose_name_plural = "WP User Meta"
#
#     def __str__(self):
#         return f"{self.user_id}: {self.meta_key} -> {self.meta_value}"
#
#
# class Family(models.Model):
#     registrant = models.OneToOneField(
#         get_user_model(),
#         on_delete=models.CASCADE,
#     )
#     family_name = models.CharField("Family Name", max_length=70, default='Please update.')
#     photo_consent = models.BooleanField("Photo consent?", default=False)
#
#     class Meta:
#         ordering = ["photo_consent"]
#         verbose_name_plural = "Families"
#
#     def __str__(self):
#         return self.family_name
#
#
# def unique_wp_member_id():
#     # For generating a random wp_member_id in FamilyMember
#     #random.seed(datetime.now().timestamp())
#     #return "non-wp-" + ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
#     #return datetime.now().strftime('%s')
#     #return "non-wp-" + str(uuid.uuid4())[-12:]
#     return  "non-wp-" + ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))


class FamilyMember(models.Model):
    family = models.ForeignKey(
        get_user_model(),
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
    # Note: Unique can be True and Null will work, but cannot have empty field entry, that will violate Unique constraint.
#    wp_member_id = models.CharField("WP Member ID", max_length=20, null=True, blank=True, unique=True, default=unique_wp_member_id())
    diet_req = models.BooleanField("Dietary requirements?", default = False )
    diet_detail = models.TextField("Dietary requirements", max_length=1024, null=True, blank=True)
    medical_req = models.BooleanField("Medical needs?", default = False )
    medical_detail = models.TextField("Medical details", max_length=1024, null=True, blank=True)

    # def get_absolute_url(self):
    #     return reverse("users:detail", kwargs={"username": self.username})

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.type = self.base_type
        return super().save(*args, **kwargs)

    def clean(self):
        errors = {}
        if self.diet_req and not self.diet_detail:
            errors["diet_detail"] = "If Dietary Requirements is ticked, Dietary Details must be filled in."

        if self.medical_req and not self.medical_detail:
            errors["medical_detail"] = "If Medical Requirements is ticked, Medical Details must be filled in."

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return self.full_name


class ParentManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=FamilyMember.Types.PARENT)


class ChildManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=FamilyMember.Types.CHILD)


class ParentMore(models.Model):
    family_member = models.OneToOneField(FamilyMember, on_delete=models.CASCADE)
    # We don't need to hold this information, according to Flo. They will be just with the Registrant.
    # contact_number = models.CharField('Contact Number', max_length=20, null=True, blank=True)
    # email_address = models.EmailField('E-mail Address', max_length=255, null=True, blank=True)

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

    # def __str__(self):
    #     return self.full_name


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
    fsm = models.BooleanField("Free School Meal", default = False )
    sen_req = models.BooleanField("SEN Requirements?", default = False )
    sen_detail = models.TextField("SEN Requirements", max_length=1024, null=True, blank=True)

    @property
    def years_old(self):
        date_diff = relativedelta(datetime.today(), self.dob)
        #years_old = date_diff.years
        # print(f"I was born in {self.more.dob}. I am {years_old} years old.")
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
        child = self.years_old in range(4, 11)
        return child

    @property
    def is_youngster(self):
        youngster = self.years_old < 4
        return youngster

    @property
    def is_post_teen(self):
        # Funding is only up to 16, so this will show how many are set as Child but over 16.
        post_teen = self.years_old > 16
        return post_teen

    @property
    def is_time_traveller(self):
        # DoB is in the future!
        time_traveller = self.dob > datetime.now().date()
        return time_traveller

    @property
    def is_too_old(self):
        # DoB makes them older than 25! Become an Adult (Parent)!
        too_old = self.years_old > 25
        return too_old

    @property
    def is_immortal(self):
        # DoB makes them older than 100!
        immortal = self.years_old > 99
        return immortal

    def clean(self):
        errors = {}
        if self.sen_req and not self.sen_detail:
            errors["sen_detail"] = "If SEN Requirements is ticked, SEN Details must be filled in."

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.dob} - {self.gender} - {self.fsm}"
#        return self.family_member.full_name


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

    @property
    def age(self):
        date_diff = relativedelta(datetime.today(), self.more.dob)
        #years_old = date_diff.years
        # print(f"I was born in {self.more.dob}. I am {years_old} years old.")
        return date_diff.years


    # Note, the following properties do not work with Queryset filters.
    # May need to use a Manager to do that instead.

    # @property
    # def is_teenager(self):
    #     teenager = self.years_old() in range(11, 17)
    #     return teenager
    #
    # @property
    # def is_child(self):
    #     # This definition of child is a Child between 4 and 10 (as required by reports)
    #     child = self.years_old() in range(4, 10)
    #     return child
    #
    # @property
    # def is_youngster(self):
    #     youngster = self.years_old() < 4
    #     return youngster