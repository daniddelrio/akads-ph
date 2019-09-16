from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import Tutor, Tutee

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

#class TutorRegisterForm1(UserCreationForm):
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
