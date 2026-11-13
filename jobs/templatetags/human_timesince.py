import datetime
from django import template
from django.utils import timezone

register = template.Library()

@register.filter(name='human_timesince')
def human_timesince(value):
    """Return a human readable ``timesince`` limited to the largest unit.
    Examples: ``5 weeks ago``, ``2 days ago``, ``3 months ago``.
    """
    if not isinstance(value, (datetime.datetime, datetime.date)):
        return ''
    now = timezone.now()
    if isinstance(value, datetime.date) and not isinstance(value, datetime.datetime):
        # treat date as midnight
        value = datetime.datetime.combine(value, datetime.time.min, tzinfo=timezone.get_current_timezone())
    delta = now - value
    seconds = int(delta.total_seconds())
    # Compute in order: years, months (approx 30 days), weeks, days, hours, minutes
    intervals = (
        ('year', 31536000),
        ('month', 2592000),
        ('week', 604800),
        ('day', 86400),
        ('hour', 3600),
        ('minute', 60),
    )
    for name, count in intervals:
        amount = seconds // count
        if amount >= 1:
            return f"{amount} {name}{'s' if amount != 1 else ''} ago"
    return 'just now'
