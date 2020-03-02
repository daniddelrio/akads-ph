from django.core.mail import send_mail
from decouple import config

EMAIL_FROM = config('EMAIL_HOST_USER')

def send_confirmed_session(session, amount):
	EMAIL_TO = session.user.email

	message = """Session has been confirmed. You may find the details here:
	Tutor: {}
	Tutee: {}
	Location: {}
	Subject: Grade {} {}
	Date and Time: {}, {} - {}
	Amount: PHP {}
	""".format(
		session.tutor,
		session.user,
		session.location,
		session.grade,
		session.subject,
		session.session_date,
		session.time_start,
		session.time_end,
		amount,
	)

	subject = 'Session #{}: Tutor {} and Tutee {} - {}'.format(
		session.pk,
		session.tutor,
		session.user,
		session.session_date,
	)

	try:
		send_mail(
		    subject,
		    message,
		    EMAIL_FROM,
		    [EMAIL_TO],
		    fail_silently=False,
		)
	except Exception as ex:
		template = "An exception of type {0} occurred. Arguments:\n{1!r}"
		print(template.format(type(ex).__name__, ex.args))
