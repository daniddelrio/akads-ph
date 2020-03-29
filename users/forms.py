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
