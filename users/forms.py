from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import *
from django.forms import ModelForm

User = get_user_model()


class PictureForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PictureForm, self).__init__(*args, **kwargs)
        self.fields["picture"].widget.attrs = {
            "id": "display-pic",
            "style": "opacity: 0;",
        }

    class Meta:
        model = User
        fields = ["picture"]


class TuteeRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_tutee = True
        user.save()
        tutee = Tutee.objects.create(user=user)
        return user


class RequestScheduleForm(ModelForm):
    SCHED_CHOICES = (
        ("7:00 am - 7:30 am", "sevenToHalf"),
        ("7:30 am - 8:00 am", "halfToEight"),
        ("8:00 am - 8:30 am", "eightToHalf"),
        ("8:30 am - 9:00 am", "halfToNine"),
        ("9:00 am - 9:30 am", "nineToHalf"),
        ("9:30 am - 10:00 am", "halfToTen"),
        ("10:00 am - 10:30 am", "tenToHalf"),
        ("10:30 am - 11:00 am", "halfToEleven"),
        ("11:00 am - 11:30 am", "elevenToHalf"),
        ("11:30 am - 12:00 nn", "halfToTwelve"),
        ("12:00 nn - 12:30 pm", "twelveToHalf"),
        ("12:30 pm - 1:00 pm", "halfToThirteen"),
        ("1:00 pm - 1:30 pm", "thirteenToHalf"),
        ("1:30 pm - 2:00 pm", "halfToFourteen"),
        ("2:00 pm - 2:30 pm", "fourteenToHalf"),
        ("2:30 pm - 3:00 pm", "halfToFifteen"),
        ("3:00 pm - 3:30 pm", "fifteenToHalf"),
        ("3:30 pm - 4:00 pm", "halfToSixteen"),
        ("4:00 pm - 4:30 pm", "sixteenToHalf"),
        ("4:30 pm - 5:00 pm", "halfToSevenTeen"),
        ("5:00 pm - 5:30 pm", "seventeenToHalf"),
        ("5:30 pm - 6:00 pm", "halfToEighteen"),
        ("6:00 pm - 6:30 pm", "eighteenToHalf"),
        ("6:30 pm - 7:00 pm", "halfToNineteen"),
    )
    session_schedule = forms.MultipleChoiceField(
        choices=SCHED_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="id_session_schedule",
    )

    class Meta:
        model = Sessions
        fields = ["session_schedule"]


class MutualScheduleForm(forms.Form):
    def __init__(self, sched_choices, *args, **kwargs):
        super(MutualScheduleForm, self).__init__(*args, **kwargs)
        self.fields["session_mutual"].choices = sched_choices

    session_mutual = forms.MultipleChoiceField(choices=(), required=True)


# class TutorRegisterForm1(UserCreationForm):
#    firstname = forms.CharField()
#    lastname = forms.CharField()
#    email = forms.EmailField()

#    class Meta:
#        model = User
#        fields = ['username', 'firstname', 'lastname', 'password1', 'password2', 'email']

# class TutorRegisterForm2(UserCreationForm):
#    location = forms.CharField()

#    class Meta:
#        model = User
#        fields = ['location']

#    @transaction.atomic
#    def save(self):
#        user = super().save(commit=False)
#        user.is_tutor = True
#        user.save()
#        tutor = Tutor.objects.create(user=user)
#        return user
