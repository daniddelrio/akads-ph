from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Tutor, Tutee, User, Locations, Sessions, Sessions_Accepted, Sessions_Ended, Transaction, Requests, Rating, Subjects, Bookings
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.contrib.auth import update_session_auth_hash

import datetime

def register_tutee(request):
    if (request.method == 'POST'):
        try:
            new_username = request.POST.get('username')
            new_firstname = request.POST.get('firstname')
            new_lastname = request.POST.get('lastname')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            new_email = request.POST.get('email')
            new_housenum = request.POST.get('housenum')
            new_province = request.POST.get('province')
            new_city = request.POST.get('city')
            new_barangay = request.POST.get('barangay')
            new_cellnum = request.POST.get('cellnum')
            new_birthday = request.POST.get('birthday')
            new_sex = request.POST.get('sex')
            new_bio = request.POST.get('bio')
            new_cardnum = request.POST.get('cardnum')
            new_fullname = request.POST.get('fullname')
            new_expiry_date = request.POST.get('expiry_date')
            new_seccode = request.POST.get('seccode')
            if(password1 == password2):
                new_password = request.POST.get('password1')
                user = User.objects.create_user(username=new_username, first_name=new_firstname, last_name=new_lastname, password=new_password, email=new_email, is_tutee=True)
                tutee = Tutee.objects.create(user=user, housenum=new_housenum, province=new_province, city=new_city, barangay=new_barangay, cellnum=new_cellnum, birthday=new_birthday, sex=new_sex, bio=new_bio, cardnum=new_cardnum, fullname=new_fullname, expiry_date=new_expiry_date, seccode=new_seccode)
                messages.success(request, f'Account created!')
                return render(request, "users/tutee/registertutee.html")
            else:
                messages.error(request, 'Error passwords did not match each other')
                return render(request, "users/tutee/registertutee.html")
            return render(request, "users/tutee/registertutee.html")
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            messages.error(request, 'Error please input valid values for each field')
            return render(request, "users/tutee/registertutee.html")
    else:
        return render(request, "users/tutee/registertutee.html")

def register_tutor(request):
    if (request.method == 'POST'):
        try:
            new_username = request.POST.get('username')
            new_firstname = request.POST.get('firstname')
            new_lastname = request.POST.get('lastname')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            new_email = request.POST.get('email')
            new_location = request.POST.get('location')
            new_birthday = request.POST.get('birthday')
            new_sex = request.POST.get('sex')
            new_subjects = request.POST.get('subjects')
            new_bio = request.POST.get('bio')
            new_reason = request.POST.get('reason')
            new_requirements = request.POST.get('uploadfiles')
            if(password1 == password2):
                new_password = request.POST.get('password1')
                user = User.objects.create_user(username=new_username, first_name=new_firstname, last_name=new_lastname, password=new_password, email=new_email)
                tutor = Tutor.objects.create(user=user, birthday=new_birthday, sex=new_sex, bio=new_bio, reason=new_reason, requirements=new_requirements)
                new_location1 = new_location.split(",")
                print(new_location1)
                for x in new_location1:
                    location = Locations.objects.create(user=user, location=x)

                print(new_subjects)
                new_subject1 = new_subjects.split(",")
                print(new_subject1)
                for x in new_subject1:
                    subject = Subjects.objects.create(user=user, subjects=x)

                messages.success(request, f'Account created!')
                return render(request, "users/tutor/registertutor.html")
            else:
                messages.error(request, 'Error passwords did not match each other')
                return render(request, "users/tutor/registertutor.html")
            return render(request, "users/tutor/registertutor.html")
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            messages.error(request, 'Error please input valid values for each field')
            return render(request, "users/tutor/registertutor.html")
    else:
        return render(request, "users/tutor/registertutor.html")

def login_user(request):
    if(request.method == 'POST'):
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username = username, password = password)

            if (user is not None):
                login(request, user)
                return redirect(reverse('home'))
            else:
                messages.error(request, 'Please enter a valid username-password combination')
                return render(register, "users/login.html")
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            #messages.error(request, 'Error please input valid values for each field')
            return render(request, "users/login.html")

    return render(request, "users/login.html")

@login_required
def home(request):
    user=request.user
    credit_user = User.objects.get(id=user.id)
    if(user.is_tutee==True):
        user2 = Tutee.objects.get(user=user)
        sessions_acc = Sessions_Accepted.objects.filter(tutee = user)
        if(request.method == 'POST'):
            try:
                session_num = len(Sessions_Accepted.objects.filter(tutee = user))

                new_grade = request.POST.get('grade')
                new_date = request.POST.get('date')
                new_start = request.POST.get('start_time')
                new_location = request.POST.get('location')
                new_hours = request.POST.get('hours')
                new_subject = request.POST.get('subject')
                new_end = request.POST.get('end_time')

                orders = Sessions.objects.filter(user=user)
                new_code = get_random_string(length=5)
                print('made it here0')
                
                new_dates = new_date.split(",")
                credit_cost = len(new_dates) * int(new_hours)

                if user.credits < credit_cost:
                    plurality = 's' if credit_cost > 1 else ''
                    messages.error(request, f"You don't have enough credits! (You need {credit_cost} credit{plurality})")

                try:
                    for _date in new_dates:
                        new_sessions = Sessions.objects.create(user=user, grade=new_grade, time_start=new_start, hours=new_hours, location=new_location, code=new_code, subject=new_subject, time_end=new_end, session_date=_date)
                except Exception as ex:
                    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    print(message)

                user.credits -= credit_cost
                user.save()
                
                print('made it here')

                # Commented out for now. - Carlos
                # new_booking = new_date.split(",")
                # for z in new_booking:
                #     book = Bookings.objects.create(session=new_sessions, dates=z)

                loc = Locations.objects.filter(location=new_location)
                subjects = Subjects.objects.filter(subjects=new_subject)
                for x in loc:
                    for y in subjects:
                        if(x.user == y.user):
                            req = Requests.objects.create(user=x.user, session=new_sessions)
                messages.success(request, f'Your request has been sent!')
                return render(request, "users/tutee/tutee_home.html", {'current_user':user2, 'sessions_acc':sessions_acc, 'credit_user':credit_user})
            except:
                session_num = len(Sessions_Accepted.objects.filter(tutee = user))

                messages.error(request, 'Error please input valid values for each field')
                return render(request, "users/tutee/tutee_home.html", {'current_user':user2, 'sessions_acc':sessions_acc, 'credit_user':credit_user})
        else:
            return render(request, 'users/tutee/tutee_home.html', {'current_user':user2, 'sessions_acc':sessions_acc, 'credit_user':credit_user})
    else:
        if(request.method == 'POST'):
            _sessions = Sessions.objects.filter(code=request.POST.get('code'))
            if len(_sessions) == 0:
                messages.error(request, "You entered an invalid code")
            else:
                _credits = 0
                for _session in _sessions:
                    _credits += _session.hours
                messages.error(request, f"{_credits} credits redeemed!")
                user.credits += _credits
                user.save()
                _sessions.delete()
        # Get multiple dates per request (if multiple)
        _requests = Requests.objects.filter(is_rejected = False, user=user)
        for _request in _requests:
            # Get all sessions with the same code
            _request.sessions = sorted(Sessions.objects.filter(code=_request.session.code), key=lambda x : x.session_date)

        sessions_acc = Sessions_Accepted.objects.filter(tutor = user)

        return render(request, "users/tutor/tutor_home.html", {'session_group':_requests, 'sessions_acc':sessions_acc, 'credit_user':credit_user})

@login_required
def upcoming(request):
    user=request.user
    credit_user = User.objects.get(id=user.id)
    if(user.is_tutee==True):
        sessions = sorted(Sessions_Accepted.objects.filter(tutee = user), key=lambda x : x.session.session_date)
        sessions_acc = sorted(Sessions_Accepted.objects.filter(tutee = user), key=lambda x : x.session.session_date)
        return render(request, "users/tutee/upcoming_tutee.html", {'session_group':sessions, 'sessions_acc':sessions_acc, 'credit_user':credit_user})
    else:
        sessions = sorted(Sessions_Accepted.objects.filter(tutor = user), key=lambda x : x.session.session_date)
        sessions_acc = sorted(Sessions_Accepted.objects.filter(tutor = user), key=lambda x : x.session.session_date)
        count = 1
        tutee_now = []
        for x in sessions:
            tutee_now = Tutee.objects.get(user=x.tutee).cellnum

        if(tutee_now is not None):
            return render(request, "users/tutor/upcoming_tutor.html", {'session_group':sessions, 'sessions_acc':sessions_acc, 'credit_user':credit_user, 'cellnum':tutee_now}, {'count':count})
        else:
            return render(request, "users/tutor/upcoming_tutor.html", {'session_group':sessions, 'sessions_acc':sessions_acc, 'credit_user':credit_user}, {'count':count})

@login_required
def pending(request):
    user=request.user
    credit_user = User.objects.get(id=user.id)
    sessions = Sessions.objects.filter(is_accepted = False)
    sessions2 = sessions.filter(user=user)
    sessions_acc = Sessions_Accepted.objects.filter(tutee = user)
    return render(request, "users/tutee/pending.html", {'session_group':sessions2, 'sessions_acc':sessions_acc, 'credit_user':credit_user})

@login_required
def cancel_pending(request, session_id):
    user=request.user
    sessions = Sessions.objects.get(id=session_id)
    sessions.delete()
    return redirect('home')

@login_required
def accept_tutee(request, session_id):
    user = request.user
    current_user = User.objects.get(id=user.id)
    chosen_session = Sessions.objects.get(id=session_id)
    chosen_sessions = Sessions.objects.filter(code=chosen_session.code)
    tutee = chosen_session.user

    for _session in chosen_sessions:
        _session.is_accepted = True
        _session.save()

    chosen_request = Requests.objects.filter(session=chosen_session)
    for x in chosen_request:
        x.is_rejected = True
        x.save()

    new_tutor = current_user
    new_tutee = tutee

    for _session in chosen_sessions:
        foo = Sessions_Accepted.objects.create(session=_session, tutor=new_tutor, tutee=new_tutee)

    return redirect('home')

@login_required
def delete_request(request, session_id):
    user = request.user
    sessions = Sessions.objects.get(id=session_id)
    sessions_here = Requests.objects.filter(session=sessions, user=user)

    sessions_here.delete()

    return redirect('home')

@login_required
def end_session(request, session_id):
    user=request.user
    user.credits = user.credits - 500

    new_session = Sessions.objects.get(id=session_id)
    done = Sessions_Accepted.objects.get(session=new_session)

    new_user = new_session.user
    new_tutor = done.tutor

    transaction = Transaction.objects.create(user=new_user, tutor=new_tutor, amount=500, credits=-500)

    new_id = new_session.id
    new_grade = new_session.grade
    new_subject = new_session.subject
    new_time_start = new_session.time_start
    new_time_end = new_session.time_end
    new_session_date = new_session.session_date
    new_location = new_session.location

    ended = Sessions_Ended.objects.create(session_id=new_id, user=new_user, grade=new_grade, subject=new_subject, time_start=new_time_start, time_end=new_time_end, session_date=new_session_date, location=new_location, tutor=new_tutor)
    new_session.delete()
    return redirect('upcoming')

@login_required
def confirm_session(request):
    try:
        user=request.user
        code_input = request.POST.get('code')
        new_code = Sessions.objects.get(code=code_input)

        if(new_code is not None):
            new_code.delete()
            user.credits = user.credits + 1
            return redirect('home')
        else:
            messages.error(request, 'Error please input a valid code')
            return redirect('home')
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        messages.error(request, 'Error please input a valid code')
        return redirect('home')

@login_required
def credits(request):
    user = request.user
    credit_user = User.objects.get(id=user.id)
    transaction_group = Transaction.objects.filter(user=user)
    if(user.is_tutee == True):
        sessions_acc = Sessions_Accepted.objects.filter(tutee = user)
        if(request.method == 'POST'):
            try:
                credit_user = User.objects.get(id=user.id)
                user_credits = int(request.POST.get('credits'))
                credit_user.credits = credit_user.credits + user_credits
                credit_user.save()

                transactions = Transaction.objects.create(user=user, credits=user_credits, amount=user_credits)
                transaction_group = Transaction.objects.filter(user=user)
                return render(request, "users/credits_page_tutee.html", {'credit_user':credit_user, 'transaction_group':transaction_group, 'sessions_acc':sessions_acc})
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print(message)
                return render(request, "users/credits_page_tutee.html", {'credit_user':credit_user, 'transaction_group':transaction_group, 'sessions_acc':sessions_acc})
        return render(request, "users/credits_page_tutee.html", {'credit_user':credit_user, 'transaction_group':transaction_group, 'sessions_acc':sessions_acc})
    else:
        transaction_group = Transaction.objects.filter(tutor=user)
        sessions_acc = Sessions_Accepted.objects.filter(tutor = user)

        return render(request, "users/credits_page_tutor.html", {'credit_user':credit_user, 'transaction_group':transaction_group, 'sessions_acc':sessions_acc})


@login_required
def history(request):
    user=request.user
    credit_user = User.objects.get(id=user.id)
    if(user.is_tutee==True):
        sessions = Sessions_Ended.objects.filter(user=user)
        sessions_acc = Sessions_Accepted.objects.filter(tutee = user)
        return render(request, "users/tutee/history_tutee.html", {'session_group':sessions, 'sessions_acc':sessions_acc, 'credit_user':credit_user})
    else:
        sessions = Sessions_Ended.objects.filter(tutor=user)
        sessions_acc = Sessions_Accepted.objects.filter(tutor = user)
        return render(request, "users/tutor/history_tutor.html", {'session_group':sessions, 'sessions_acc':sessions_acc, 'credit_user':credit_user})

def landing(request):
    return render(request, 'users/landing.html')

def tutor_tutee(request):
    return render(request, 'users/register.html')

@login_required
def edit_password(request):
    user = request.user
    credit_user = User.objects.get(id=user.id)
    if (user.is_tutee==True):
        sessions_acc = Sessions_Accepted.objects.filter(tutee = user)
    else:
        sessions_acc = Sessions_Accepted.objects.filter(tutor = user)

    if (request.method == 'POST'):
        try:
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            old_password = request.POST.get('old_password')

            if(new_password1 == new_password2 and user.check_password(old_password)):
                user.set_password(new_password1)
                user.save()
                return redirect('profile')
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            messages.error(request, 'Error please input valid values for each field')
            return render(request, 'users/edit_password.html', {'sessions_acc':sessions_acc, 'credit_user':credit_user})
    return render(request, 'users/edit_password.html', {'sessions_acc':sessions_acc, 'credit_user':credit_user})

@login_required
def edit_location(request):
    user = request.user
    credit_user = User.objects.get(id=user.id)
    if(user.is_tutee==True):
        sessions_acc = Sessions_Accepted.objects.filter(tutee = user)
        if (request.method == 'POST'):
            try:
                tutee = Tutee.objects.get(user=user)
                new_housenum = request.POST.get('housenum')
                new_province = request.POST.get('province')
                new_barangay = request.POST.get('barangay')
                new_city = request.POST.get('city')

                tutee.housenum = new_housenum
                tutee.province = new_province
                tutee.barangay = new_barangay
                tutee.city = new_city

                tutee.save()
                return redirect('profile')
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print(message)
                messages.error(request, 'Error please input valid values for each field')
                if(user.is_tutee==True):
                    return render(request, 'users/edit_location_tutee.html', {'sessions_acc':sessions_acc, 'credit_user':credit_user})
                else:
                    return render(request, 'users/edit_location_tutor.html', {'sessions_acc':sessions_acc, 'credit_user':credit_user})
    else:
        sessions_acc = Sessions_Accepted.objects.filter(tutor = user)
        if (request.method == 'POST'):
            try:
                tutor = Tutor.objects.get(user=user)
                loc = Locations.objects.filter(user=user)
                new_location = request.POST.get('location')

                new_location1 = new_location.split(",")
                loc.delete()
                print(new_location1)
                for x in new_location1:
                    location = Locations.objects.create(user=user, location=x)
                    location.save()

                return redirect('profile')
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print(message)
                messages.error(request, 'Error please input valid values for each field')
                if(user.is_tutee==True):
                    return render(request, 'users/edit_location_tutee.html', {'sessions_acc':sessions_acc, 'credit_user':credit_user})
                else:
                    return render(request, 'users/edit_location_tutor.html', {'sessions_acc':sessions_acc, 'credit_user':credit_user})
    if(user.is_tutee==True):
        return render(request, 'users/edit_location_tutee.html', {'sessions_acc':sessions_acc, 'credit_user':credit_user})
    else:
        return render(request, 'users/edit_location_tutor.html', {'sessions_acc':sessions_acc, 'credit_user':credit_user})

@login_required
def edit_card(request):
    user = request.user
    credit_user = User.objects.get(id=user.id)
    sessions_acc = Sessions_Accepted.objects.filter(tutee = user)
    try:
        if (request.method == 'POST'):
            tutee = Tutee.objects.get(user=user)
            new_cardnum = request.POST.get('cardnum')
            new_fullname = request.POST.get('fullname')
            new_expiry_date = request.POST.get('expiry_date')
            new_seccode = request.POST.get('seccode')

            tutee.cardnum = new_cardnum
            tutee.fullname = new_fullname
            tutee.expiry_month = new_expiry_date
            tutee.seccode = new_seccode

            tutee.save()
            return redirect('profile')
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        messages.error(request, 'Error please input valid values for each field')
        return render(request, 'users/edit_card.html', {'sessions_acc':sessions_acc, 'credit_user':credit_user})
    return render(request, 'users/edit_card.html', {'sessions_acc':sessions_acc, 'credit_user':credit_user})


@login_required
def profile(request):
    user=request.user
    credit_user = User.objects.get(id=user.id)
    if(user.is_tutee==True):
        user2 = Tutee.objects.get(user=user)
        sessions_acc = Sessions_Accepted.objects.filter(tutee = user)
        return render(request, 'users/profile.html', {'current_user':user2, 'sessions_acc':sessions_acc, 'credit_user':credit_user})
    else:
        loc = Locations.objects.filter(user=user)
        user2 = Tutor.objects.get(user=user)
        sessions_acc = Sessions_Accepted.objects.filter(tutor = user)
    return render(request, 'users/profile.html', {'current_user':user2, 'location_user':loc, 'sessions_acc':sessions_acc, 'credit_user':credit_user})


def booking(request):
    user=request.user
    if(request.method == 'POST'):
        try:
            return redirect('home')
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            messages.error(request, 'Error please input valid values for each field')
            return redirect('home')
    else:
        return render(request, 'users/tutee/tutee_home.html')


def rating(request, session_id):
    user=request.user
    if(request.method == 'POST'):
        try:
            if(user.is_tutee == True):
                new_stars = request.POST.get('stars')
                new_user = Sessions.objects.get(id=session_id)
                new_comments = request.POST.get('comments')
                rate = Rating.objects.create(stars=new_stars, user=user, comments=new_comments)
            return render('home')
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            messages.error(request, 'Error please input valid values for each field')
            return redirect('home')
    else:
        return redirect('home')

def accepted(request):
    user = request.user
    if(user.is_tutee == True):
        sessions_set = Sessions_Accepted.objects.filter(tutee=user)
        sessions = Count(sessions_set)
        print("BITCHEZ")
        print(sessions)
    else:
        sessions_set = Sessions_Accepted.objects.filter(tutor=user)
        sessions = Count(sessions_set)
        print("BITCHEZ")
        print(sessions)
    return render(request, "users/base.html", {'sessions_group':sessions})
