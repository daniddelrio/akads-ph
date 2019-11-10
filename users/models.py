from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    is_tutee = models.BooleanField(default=False)
    credits = models.IntegerField(default=0)

    def __str__(self):
        return self.username

class Tutor(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = "tutor")
    birthday = models.DateField()
    sex = models.CharField(max_length=7)
    bio = models.CharField(max_length=100)
    reason = models.CharField(max_length=100, null=True)
    requirements = models.ImageField(blank=True)

    def __str__(self):
        return self.user.username

class Tutee(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = "tutee")
    housenum = models.CharField(max_length=100)
    province = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    barangay = models.CharField(max_length=50)
    cellnum = models.CharField(max_length=13)
    birthday = models.DateField()
    sex = models.CharField(max_length=7)
    bio = models.CharField(max_length=100)
    cardnum = models.CharField(max_length=16)
    fullname = models.CharField(max_length=30)
    expiry_date = models.CharField(max_length=7)
    seccode = models.IntegerField()

    def __str__(self):
        return self.user.username

class Locations(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "locations")
    location = models.CharField(max_length=1000)

    def __str__(self):
        return self.user.username

class Sessions(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "sessions")
    grade = models.IntegerField()
    subject = models.CharField(max_length=20)
    time_start = models.TimeField()
    hours = models.IntegerField()
    time_end = models.TimeField()
    session_date = models.DateField()
    location = models.CharField(max_length=50)
    code = models.CharField(max_length=5)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Sessions_Accepted(models.Model):
    session = models.ForeignKey(Sessions, on_delete=models.CASCADE, related_name = "sessions1")
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "tutor1")
    tutee = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "tutee2")

    def __str__(self):
        return self.tutee.username

class Sessions_Ended(models.Model):
    session_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "sessions_ended")
    grade = models.IntegerField()
    subject = models.CharField(max_length=20)
    time_start = models.TimeField()
    time_end = models.TimeField(blank=True, null=True)
    session_date = models.DateField()
    location = models.CharField(max_length=50)
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "tutor2")

    def __str__(self):
        return self.user.username

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "transactions")
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "transactiontutor", null = True)
    date = models.DateField(default=timezone.now)
    amount = models.IntegerField(null = True)
    credits = models.IntegerField(null = True)

    def __str__(self):
        return self.user.username

class Requests(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "sess")
    session = models.ForeignKey(Sessions, on_delete=models.CASCADE, related_name = "sessions2")
    is_rejected = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username

class Rating(models.Model):
    stars = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "rating")
    comments = models.CharField(max_length=1000)

class Subjects(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "subj")
    subjects = models.CharField(max_length=1000)

    def __str__(self):
        return self.user.username

class Bookings(models.Model):
    session = models.ForeignKey(Sessions, on_delete=models.CASCADE, related_name = 'bookings')
    dates = models.DateField()

    def __str__(self):
        return session.id
