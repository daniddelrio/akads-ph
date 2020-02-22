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