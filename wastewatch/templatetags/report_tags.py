from django import template
from wastewatch.utils import get_pending_reports_count

register = template.Library()

@register.simple_tag
def pending_reports_count():
    return get_pending_reports_count()