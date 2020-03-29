from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.contrib.auth import update_session_auth_hash
from django.db import transaction
from django.db.models import Q, Sum
from .services import *
from .forms import *
import datetime
from django.conf import settings
from .emailing import send_confirmed_session


SCHED_CHOICES = {
    "sevenToHalf": "7to730",
    "halfToEight" : "730to8",
    "eightToHalf" : "8to830",
    "halfToNine": "830to9",
    "nineToHalf" :"9to930" ,  
    "halfToTen" : "930to10" ,      
    "tenToHalf" : "10to1030" ,      
    "halfToEleven" : "1030to11",   
    "elevenToHalf" : "11to1130" ,   
    "halfToTwelve":"1130to12" ,   
    "twelveToHalf" : "12to1230" ,   
    "halfToThirteen" : "1230to13" , 
    "thirteenToHalf" : "13to1330", 
    "halfToFourteen" : "1330to14", 
    "fourteenToHalf" : "14to1430", 
    "halfToFifteen" : "1430to15",  
    "fifteenToHalf" : "15to1530",  
    "halfToSixteen" : "1530to16",  
    "sixteenToHalf":"16to1630",
    "halfToSevenTeen" : "1630to17",
    "seventeenToHalf" : "17to1730",
    "halfToEighteen" : "1730to18", 
    "eighteenToHalf" : "18to1830", 
    "halfToNineteen" : "1830to19",
}

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

    if(user.is_tutee==True):
        user2 = Tutee.objects.get(user=user)

        if Payment.objects.filter(is_paid=False, tutee=user).exists():
            messages.error(request, 'You have pending payments. Please pay these first.')
            return redirect('transactions')

        if(request.method == 'POST'):
            form = RequestScheduleForm()
            print(request.POST.getlist("session_schedule"))
            sched = request.POST.getlist("session_schedule")

            try:
                session_num = len(Sessions_Accepted.objects.filter(tutee = user))

                new_grade = request.POST.get('grade')
                new_date = request.POST.get('date')
                new_start = request.POST.get('start_time')
                new_location = request.POST.get('location')
                new_hours = request.POST.get('hours')
                new_subject = request.POST.get('subject')
                new_end = request.POST.get('end_time')
                new_sched = " ".join(sched)
                    
                print(new_sched)

                new_start = datetime.datetime.strptime(new_start, settings.TIME_INPUT_FORMATS[0]).time()

                orders = Sessions.objects.filter(user=user)
                new_code = get_random_string(length=5)
                print('made it here0')
                
                new_dates = new_date.split(",")
                credit_cost = len(new_dates) * int(new_hours)

                # if user.credits < credit_cost:
                #     plurality = 's' if credit_cost > 1 else ''
                #     messages.error(request, f"You don't have enough credits! (You need {credit_cost} credit{plurality})")

                try:
                    for _date in new_dates:
                        new_sessions = Sessions.objects.create(user=user,
                                                               grade=new_grade,
                                                               time_start=new_start,
                                                               hours=new_hours,
                                                               location=new_location,
                                                               code=new_code,
                                                               subject=new_subject,
                                                               time_end=new_end,
                                                               session_date=_date,
                                                               session_schedule = new_sched
                                                               ) 
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
            except:
                session_num = len(Sessions_Accepted.objects.filter(tutee = user))
                messages.error(request, 'Error please input valid values for each field')
        else:     
            form = RequestScheduleForm()
        
        return render(request, "users/tutee/tutee_home.html", {
            'current_user':user2, 
            'credit_user':user,
            'form': form
            })
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

        return render(request, "users/tutor/tutor_home.html", {
            'session_group':_requests,
            'credit_user':user
            })

@login_required
def upcoming(request):
    user=request.user
    credit_user = User.objects.get(id=user.id)

    if(user.is_tutee==True):
        sessions = sorted(Sessions_Accepted.objects.filter(tutee = user), key=lambda x : x.session.session_date)
        return render(request, "users/tutee/upcoming_tutee.html", {'session_group':sessions})
    else:
        sessions = sorted(Sessions_Accepted.objects.filter(tutor = user), key=lambda x : x.session.session_date)
        count = 1
        tutee_now = []
        for x in sessions:
            tutee_now = Tutee.objects.get(user=x.tutee).cellnum

        context = {
            'session_group':sessions,
            'credit_user':credit_user,
        }
        if(tutee_now is not None):
            context['cellnum'] = tutee_now

        return render(request, "users/tutor/upcoming_tutor.html", context, {'count': count})

@login_required
def pending(request):
    user = request.user

    sessions = Sessions.objects.filter(is_accepted = False, user=user)
    return render(request, "users/tutee/pending.html", {
        'session_group':sessions, 
        'credit_user':user
        })

@login_required
def cancel_pending(request, session_id):
    user=request.user
    sessions = Sessions.objects.get(id=session_id)
    sessions.delete()
    return redirect('home')

@login_required
def accept_tutee(request, session_id):
    if(request.method == "POST"):
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
    else:
        current_session = Sessions.objects.get(id = session_id)
        string_sched = current_session.session_schedule
        array_sched = string_sched.split()
        schedlist = [(SCHED_CHOICES[sched], sched) for sched in array_sched]
        print(schedlist)
        form = MutualScheduleForm(sched_choices = schedlist)
        return render(request, "users/tutor/mutual_sched.html", {"form": form,})

@login_required
def delete_request(request, session_id):
    user = request.user
    sessions = Sessions.objects.get(id=session_id)
    sessions_here = Requests.objects.filter(session=sessions, user=user)

    sessions_here.delete()

    return redirect('home')

@login_required
@transaction.atomic
def end_session(request, session_id):
    user=request.user
    ended = Sessions_Ended.objects.filter(pk=session_id)

    if not ended.exists():
        print(message)
        messages.error(request, 'Error: this session does not exist!')
        return redirect('home')

    ended = ended.first()
    if (request.method == 'POST'):
        try:

            # ============ CHANGE ONCE MAP IS BACK =============
            # new_location = request.POST.get('location')
            new_location = 'Test'
            new_time_end = request.POST.get('end_time')

            messages.success(request, f'Session has ended!')

            ended.time_end = datetime.datetime.strptime(new_time_end, "%I:%M %p").time()
            ended.save()

            minutes = ended.minutes
            amount = get_amount_from_minutes(minutes)

            if not Payment.objects.filter(session=ended).exists():
                Payment.objects.create(tutee=user, session=ended, amount=amount)

            return redirect('transactions')
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            messages.error(request, 'Error: please input valid values for each field')

    return render(request, "users/tutee/end_session.html", {
        'session' : ended,
        'credit_user': user
        })

# In the POV of the TUTOR
@login_required
def complete_session(request, session_id):
    user=request.user

    new_session = Sessions.objects.get(id=session_id)
    done = Sessions_Accepted.objects.get(session=new_session)

    new_user = new_session.user
    new_tutor = done.tutor

    new_grade = new_session.grade
    new_subject = new_session.subject
    new_time_end = new_session.time_end

    if (request.method == 'POST'):
        try:
            # ============ CHANGE ONCE MAP IS BACK =============
            # new_location = request.POST.get('location')
            new_location = 'Test'
            new_session_date = request.POST.get('date')
            new_time_start = request.POST.get('start_time')
            new_time_end = request.POST.get('end_time')

            if new_time_end <= new_time_start:
                raise Exception("Invalid time range")

            if new_session_date is None or new_time_start is None or new_time_end is None:
                raise Exception("Unfilled form fields")

            new_time_start = datetime.datetime.strptime(new_time_start, settings.TIME_INPUT_FORMATS[0]).time()
            new_time_end = datetime.datetime.strptime(new_time_end, settings.TIME_INPUT_FORMATS[0]).time()

            messages.success(request, f'Session has been completed! Please have your tutor confirm the session.')

            completed = Sessions_Ended.objects.create(
                user=new_user, 
                grade=new_grade, 
                subject=new_subject, 
                time_start=new_time_start, 
                time_end=new_time_end, 
                session_date=new_session_date, 
                location=new_location, 
                tutor=new_tutor,
                with_tutee=True
            )

            new_session.delete()
            return redirect('home')
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            messages.error(request, 'Error: please input valid values for each field')

    return render(request, "users/tutor/complete_session.html", {
        'session' : done,
        'credit_user': user
    })

@login_required
def unconfirmed(request):
    user = request.user

    sessions = Sessions_Ended.objects.filter(unconfirmed=True)
    if user.is_tutee:
        sessions = sessions.filter(user=user, with_tutee=True)
    else:
        sessions = sessions.filter(tutor=user, with_tutee=False)

    context = {
        'session_group':sessions, 
        'credit_user':user
    }

    if user.is_tutee:
        return render(request, "users/tutee/unconfirmed.html", context)

    return render(request, "users/tutor/unconfirmed.html", context)

@login_required
def unconfirmed_edit(request, session_id):
    user=request.user

    if user.is_tutee:
        return redirect('home')

    if not Sessions_Ended.objects.filter(pk=session_id).exists():
        messages.error(request, 'Error: this session does not exist!')
        return redirect('home')

    session = Sessions_Ended.objects.get(pk=session_id)

    if session.final or not session.unconfirmed:
        messages.error(request, 'Error: this session is already confirmed!')
        return redirect('home')

    if (request.method == 'POST'):
        try:
            new_session_date = request.POST.get('date')
            new_time_start = request.POST.get('start_time')
            new_time_end = request.POST.get('end_time')

            if new_time_end <= new_time_start:
                raise Exception("Invalid time range")

            if new_session_date is None or new_time_start is None or new_time_end is None:
                raise Exception("Unfilled form fields")

            new_time_start = datetime.datetime.strptime(new_time_start, settings.TIME_INPUT_FORMATS[0]).time()
            new_time_end = datetime.datetime.strptime(new_time_end, settings.TIME_INPUT_FORMATS[0]).time()

            session.session_date = new_session_date
            session.time_start = new_time_start
            session.time_end = new_time_end
            session.unconfirmed = True
            session.with_tutee = True

            session.save()

            messages.success(request, f'Session has been edited! Please have your tutor confirm the session.')

            return redirect('home')
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            messages.error(request, ex.args[0])

    return render(request, "users/tutor/edit_session.html", {
        'session' : session,
        'credit_user': user,
        'curr_date': session.session_date,
        'curr_start': session.time_start.strftime(settings.TIME_INPUT_FORMATS[0]),
        'curr_end': session.time_end.strftime(settings.TIME_INPUT_FORMATS[0])
    })

@login_required
def unconfirmed_status(request, session_id, status):
    user = request.user

    if not user.is_tutee:
        return redirect('home')

    if not Sessions_Ended.objects.filter(pk=session_id).exists():
        messages.error(request, 'Session does not exist.')
        return redirect('home')

    session = Sessions_Ended.objects.get(pk=session_id)

    if status == 'confirm':
        session.unconfirmed = False
        session.final = True
        session.with_tutee = True
        session.save()

        minutes = session.minutes
        amount = get_amount_from_minutes(minutes)

        if not Payment.objects.filter(session=session).exists():
            Payment.objects.create(tutee=user, session=session, amount=amount)

        send_confirmed_session(session, amount)

        messages.success(request, 'Session has been confirmed! Please pay the necessary amount.')

        return redirect('transactions')

    elif status == 'decline':
        session.unconfirmed = True
        session.with_tutee = False
        session.save()

        messages.info(request, 'Session has been declined. Please wait until your tutor has corrected the details.')

    return redirect('home')

@login_required
def confirm_session(request):
    try:
        user=request.user
        code_input = request.POST.get('code')
        new_code = Sessions.objects.get(code=code_input)

        if(new_code is not None):
            new_code.delete()
            user.credits = user.credits + 1
        else:
            messages.error(request, 'Error please input a valid code')

        return redirect('home')
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        messages.error(request, 'Error please input a valid code')
        return redirect('home')

# Shows both transactions and payments needed
@login_required
def transactions(request):
    user = request.user
    if(not user.is_tutee):
        messages.error(request, 'Error: you cannot access this page.')
        return redirect('landing')

    transaction_group = Transaction.objects.filter(user=user)
    pending_payments = Payment.objects.filter(tutee=user, is_paid=False)
    completed_payments = Payment.objects.filter(tutee=user, is_paid=True)

    # Get sum of pending payments
    pending_sum = pending_payments.aggregate(Sum('amount'))['amount__sum']
    pending_sum = 0 if pending_sum is None else pending_sum
    amount_paid = transaction_group.filter(payment__is_paid=False).aggregate(Sum('amount'))['amount__sum']
    amount_paid = 0 if amount_paid is None else amount_paid
    pending_sum -= amount_paid

    return render(request, "users/transactions.html", {
        'credit_user': user, 
        'transaction_group':transaction_group,
        'pending_payments':pending_payments,
        'completed_payments':completed_payments,
        'pending_sum': pending_sum
    })

@transaction.atomic
@login_required
def pay_balance(request):
    user = request.user
    if(not user.is_tutee):
        messages.error(request, 'Error: you cannot access this page.')
        return redirect('landing')

    tutee = Tutee.objects.get(user=user)
    transaction_group = Transaction.objects.filter(user=user)
    pending_payments = Payment.objects.filter(tutee=user, is_paid=False)

    # Get sum of pending payments
    pending_sum = pending_payments.aggregate(Sum('amount'))['amount__sum']
    pending_sum = 0 if pending_sum is None else pending_sum
    amount_paid = transaction_group.filter(payment__is_paid=False).aggregate(Sum('amount'))['amount__sum']
    amount_paid = 0 if amount_paid is None else amount_paid
    pending_sum -= amount_paid

    if(request.method == 'POST'):
        try:
            current_payment = pending_payments.first()
            session = current_payment.session

            card_number = int(request.POST.get('cardnum'))
            full_name = request.POST.get('fullname')
            exp_date = request.POST.get('expiry_date')
            security_code = int(request.POST.get('seccode'))
            amount = int(request.POST.get('amount'))

            exp_arr = exp_date.split('/')
            exp_month = int(exp_arr[0])
            exp_year = int(exp_arr[1][2:])

            tutor_name = session.tutor.first_name + ' ' + session.tutor.last_name

            token = create_token(number=card_number, exp_month=exp_month, exp_year=exp_year, cvc=security_code)
            if 'errors' in token and token['errors'][0]['status'] == '400':
                messages.error(request, token['errors'][0]['detail'])
                return render(request, "users/pay_balance.html", {
                    'credit_user':credit_user, 
                    'tutee': tutee,
                    'transaction_group':transaction_group,
                    'pending_payments':pending_payments,
                    'pending_sum': pending_sum
                })
            payment = create_payment(token_id=token['data']['id'], amount=amount, tutor_name=tutor_name, date=session.session_date)

            transaction = Transaction.objects.create(user=user, payment=current_payment, amount=amount)
            amount_paid_current = Transaction.objects.filter(payment=current_payment).aggregate(current_amount=Sum('amount'))['current_amount']

            # If tutee has already paid the pending amount, then mark it
            if amount_paid_current >= current_payment.amount:
                current_payment.is_paid = True
                current_payment.save()

            return redirect('transactions')
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            messages.error(request, 'Error: Something went wrong. Please check your inputs again.')

    return render(request, "users/pay_balance.html", {
        'credit_user': user, 
        'tutee': tutee,
        'transaction_group':transaction_group,
        'pending_payments':pending_payments,
        'pending_sum': pending_sum
    })

@login_required
def history(request):
    user=request.user
    sessions = Sessions.objects.filter(is_accepted = False, user=user)

    context = {
        'session_group':sessions,
        'credit_user':user
    }
    if(user.is_tutee==True):
        return render(request, "users/tutee/history_tutee.html", context)

    return render(request, "users/tutor/history_tutor.html", context)

def landing(request):
    return render(request, 'users/landing.html')

def tutor_tutee(request):
    return render(request, 'users/register.html')

@login_required
def edit_password(request):
    user = request.user

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

    return render(request, 'users/edit_password.html', {'credit_user':user})

@login_required
def edit_location(request):
    user = request.user
    context = {'credit_user' : user}
    if(user.is_tutee==True):
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

        return render(request, 'users/edit_location_tutee.html', context)
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

        return render(request, 'users/edit_location_tutor.html', context)

@login_required
def edit_card(request):
    user = request.user
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

    return render(request, 'users/edit_card.html', {'credit_user':user})


@login_required
def profile(request):
    user=request.user
    if(user.is_tutee==True):
        user2 = Tutee.objects.get(user=user)
    else:
        loc = Locations.objects.filter(user=user)
        user2 = Tutor.objects.get(user=user)

    return render(request, 'users/profile.html', {
        'current_user':user2, 
        'location_user':loc, 
        'credit_user':user
        })

@login_required
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

def accepted(request):
    user = request.user
    if(user.is_tutee == True):
        sessions_set = Sessions_Accepted.objects.filter(tutee=user)
        sessions = Count(sessions_set)
        print(sessions)
    else:
        sessions_set = Sessions_Accepted.objects.filter(tutor=user)
        sessions = Count(sessions_set)
        print(sessions)

    return render(request, "users/base.html", {'sessions_group':sessions})
