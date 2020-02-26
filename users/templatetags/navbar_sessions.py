from django import template
from django.db.models import Q
from users.models import Sessions_Ended, Sessions_Accepted

register = template.Library()

@register.simple_tag
def sessions_acc(user):
	if not user.is_authenticated:
		return Sessions_Accepted.objects.none()

	sessions_acc = sorted(Sessions_Accepted.objects.filter(
		Q(tutee=user) | Q(tutor=user)
		), key=lambda x : x.session.session_date)

	return sessions_acc

@register.simple_tag
def sessions_unconfirmed(user):
	if not user.is_authenticated:
		return Sessions_Ended.objects.none()

	sessions_unconfirmed = Sessions_Ended.objects.filter(unconfirmed=True, final=False)

	if user.is_tutee:
		sessions_unconfirmed = sorted(sessions_unconfirmed.filter(with_tutee=True))
	else:
		sessions_unconfirmed = sorted(sessions_unconfirmed.filter(with_tutee=False))

	return sessions_unconfirmed