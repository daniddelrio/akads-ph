from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import datetime

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

    sevenToHalf = models.BooleanField(default = False )
    halfToEight = models.BooleanField(default = False)

    eightToHalf = models.BooleanField(default = False)
    halfToNine = models.BooleanField(default = False)

    nineToHalf = models.BooleanField(default = False)
    halfToTen = models.BooleanField(default = False)

    tenToHalf = models.BooleanField(default = False)
    halfToEleven = models.BooleanField(default = False)

    elevenToHalf = models.BooleanField(default = False)
    halfToTwelve = models.BooleanField(default = False)

    twelveToHalf = models.BooleanField(default = False)
    halfToThirteen = models.BooleanField(default = False)

    thirteenToHalf = models.BooleanField(default = False)
    halfToFourteen = models.BooleanField(default = False)

    fourteenToHalf = models.BooleanField(default = False)
    halfToFifteen = models.BooleanField(default = False)

    fifteenToHalf = models.BooleanField(default = False)
    halfToSixteen = models.BooleanField(default = False)

    seventeenToHalf = models.BooleanField(default = False)
    halfToEighteen = models.BooleanField(default = False)

    eighteenToHalf = models.BooleanField(default = False)
    halfToNineteen = models.BooleanField(default = False)

    nineteenToHalf = models.BooleanField(default = False)
    halfToTwenty = models.BooleanField(default = False)

    def getSchedArray(self):
        schedArray = [
                self.sevenToHalf,
                self.halfToEight,
                self.eightToHalf,
                self.halfToNine,
                self.nineToHalf,  
                self.halfToTen,      
                self.tenToHalf,      
                self.halfToEleven,   
                self.elevenToHalf,   
                self.halfToTwelve,   
                self.twelveToHalf,   
                self.halfToThirteen, 
                self.thirteenToHalf, 
                self.halfToFourteen, 
                self.fourteenToHalf, 
                self.halfToFifteen,  
                self.fifteenToHalf,  
                self.halfToSixteen,  
                self.seventeenToHalf,
                self.halfToEighteen, 
                self.eighteenToHalf, 
                self.halfToNineteen, 
                self.nineteenToHalf, 
                self.halfToTwenty,   
            ]
        return schedArray
    
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
    time_end = models.TimeField()
    session_date = models.DateField()
    location = models.CharField(max_length=50)
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "tutor2")
    # When the session is confirmed and the details are final
    final = models.BooleanField(default=False)
    # Whether the session is unconfirmed (to see if it appears on the Unconfirmed Sessions page)
    unconfirmed = models.BooleanField(default=True)
    # Whether the session is "with" the tutee or not, i.e. whether the unconfirmed session will appear on the tutor's side or tutee's
    with_tutee = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

    @property
    def minutes(self):
        if self.time_end:
            from datetime import timedelta
            time_start = timedelta(hours=self.time_start.hour, minutes=self.time_start.minute)
            time_end = timedelta(hours=self.time_end.hour, minutes=self.time_end.minute)
            duration = time_end - time_start
            duration_in_s = duration.total_seconds()
            return divmod(duration_in_s, 60)[0]

        return 0

# Model for connection for payment between Tutee and Session
class Payment(models.Model):
    tutee = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "payments")
    session = models.OneToOneField(Sessions_Ended, on_delete=models.CASCADE, related_name="payment")
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    fully_paid_at = models.DateTimeField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    
    def __init__(self, *args, **kwargs):
        super(Payment, self).__init__(*args, **kwargs)
        self.__is_paid = self.is_paid

    def __str__(self):
        return self.session.tutor.first_name + ' ' + self.session.tutor.last_name + " - " + str(self.session.session_date)

    def save(self, *args, **kwargs):
        if self.is_paid and not self.__is_paid:
            self.fully_paid_at = datetime.now()
        super(Payment, self).save(*args, **kwargs)    

# Model to be used by the PayMongo integration when there is a transaction
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "transactions")
    # ForeignKey because a user can choose to pay in increments for a session
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="transactions")
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

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
