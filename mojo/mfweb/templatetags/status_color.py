from django import template
from django.conf import settings

register = template.Library()
@register.filter

def status_color(label, r):
    if r['status_label'] == 'BuildSuccess':
        return '<font color="#00CC00">%s</font>' % label
    elif r['status_label'] == 'BuildFail':
        return '<font color="red">%s</font>' % label
    else:
        return label
