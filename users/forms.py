from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import *
from django.forms import ModelForm

User = get_user_model()

class TuteeRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_tutee = True
        user.save()
        tutee = Tutee.objects.create(user=user)
        return user

class RequestScheduleForm(ModelForm):
    SCHED_CHOICES = (
        ("7to730", "sevenToHalf"),
        ("730to8" , "halfToEight"),
        ("8to830" , "eightToHalf"),
        ("830to9" , "halfToNine"),
        ("9to930" , "nineToHalf"),  
        ("930to10" , "halfToTen"),      
        ("10to1030", "tenToHalf"),      
        ("1030to11", "halfToEleven"),   
        ("11to1130", "elevenToHalf"),   
        ("1130to12", "halfToTwelve"),   
        ("12to1230" , "twelveToHalf"),   
        ("1230to13", "halfToThirteen"), 
        ("13to1330" , "thirteenToHalf"), 
        ("1330to14" , "halfToFourteen"), 
        ("14to1430" , "fourteenToHalf"), 
        ("1430to15", "halfToFifteen"),  
        ("15to1530", "fifteenToHalf"),  
        ("1530to16", "halfToSixteen"),  
        ("16to1630" ,"sixteenToHalf"),
        ("1630to17", "halfToSevenTeen"),
        ("17to1730" , "seventeenToHalf"),
        ("1730to18", "halfToEighteen"), 
        ("18to1830", "eighteenToHalf"), 
        ("1830to19", "halfToNineteen"),
    )    
    session_schedule = forms.MultipleChoiceField(choices = SCHED_CHOICES, widget = forms.CheckboxSelectMultiple, required = False, label = "id_session_schedule" )
    class Meta:
        model = Sessions
        fields = [
            'session_schedule'
        ]

class MutualScheduleForm(forms.Form):
    def __init__(self, sched_choices,*args, **kwargs):
        super(MutualScheduleForm,self).__init__(*args, **kwargs)
        self.fields["session_mutual"].choices = sched_choices
    session_mutual = forms.MultipleChoiceField(choices=(), required = True)

# class tutorAvailabilitySched(ModelForm):
#     sevenToHalf = forms.BooleanField(label = "7:00am - 7:30am", initial = False, required = False)
#     halfToEight = forms.BooleanField(label = "7:30am - 8:00am", initial = False, required = False)
#     eightToHalf = forms.BooleanField(label = "8:00am - 8:30am", initial = False, required = False)
#     halfToNine = forms.BooleanField(label = "8:30am - 9:00am", initial = False, required = False)
#     nineToHalf = forms.BooleanField(label = "9:00am - 9:30am", initial = False, required = False)
#     halfToTen = forms.BooleanField(label = "9:30am - 10:00am", initial = False, required = False)     
#     tenToHalf = forms.BooleanField(label = "10:00am - 10:30am", initial = False, required = False)     
#     halfToEleven = forms.BooleanField(label = "10:30am - 11:00am", initial = False, required = False)  
#     elevenToHalf = forms.BooleanField(label = "11:00am - 11:30am", initial = False, required = False)  
#     halfToTwelve = forms.BooleanField(label = "11:30am - 12:00nn", initial = False, required = False)  
#     twelveToHalf = forms.BooleanField(label = "12:00nn - 12:30pm", initial = False, required = False)  
#     halfToThirteen = forms.BooleanField(label = "12:30pm - 1:00pm", initial = False, required = False)
#     thirteenToHalf = forms.BooleanField(label = "1:00pm - 1:30pm", initial = False, required = False)
#     halfToFourteen = forms.BooleanField(label = "1:30pm - 2:00pm", initial = False, required = False)
#     fourteenToHalf = forms.BooleanField(label = "2:00pm - 2:30pm", initial = False, required = False)
#     halfToFifteen = forms.BooleanField(label = "2:30pm - 3:00pm", initial = False, required = False) 
#     fifteenToHalf = forms.BooleanField(label = "3:00pm - 3:30pm", initial = False, required = False) 
#     halfToSixteen = forms.BooleanField(label = "3:30pm - 4:00pm", initial = False, required = False) 
#     seventeenToHalf = forms.BooleanField(label = "4:00pm - 4:30pm", initial = False, required = False)
#     halfToEighteen = forms.BooleanField(label = "4:30pm - 5:00pm", initial = False, required = False)
#     eighteenToHalf = forms.BooleanField(label = "5:00pm - 5:30pm", initial = False, required = False)
#     halfToNineteen = forms.BooleanField(label = "5:30pm - 6:00pm", initial = False, required = False)
#     nineteenToHalf = forms.BooleanField(label = "6:00pm - 6:30pm", initial = False, required = False)
#     halfToTwenty = forms.BooleanField(label = "6:30pm - 7:00pm", initial = False, required = False)


# class TutorRegisterForm1(UserCreationForm):
#    firstname = forms.CharField()
#    lastname = forms.CharField()
#    email = forms.EmailField()

#    class Meta:
#        model = User
#        fields = ['username', 'firstname', 'lastname', 'password1', 'password2', 'email']

#class TutorRegisterForm2(UserCreationForm):
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
