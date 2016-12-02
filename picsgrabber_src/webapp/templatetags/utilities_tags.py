
from django import template
from django.utils.safestring import mark_safe as safe
from datetime import date, datetime, timedelta
from django.conf import settings
from django.utils.encoding import smart_str, force_unicode
from django.utils.safestring import mark_safe
from imgurpython import ImgurClient
# from webapp.models import PollerStatus, MasterTicketTotals, MasterTicketComputers

register = template.Library()


@register.simple_tag
def link_formatter(link):
    new_link = link[:-4] + 'm' + link[-4:]
    return new_link


@register.simple_tag
def gif_formatter(link):
    if link[-5] == 'h' and link[-12] != '/':
        new_link = link[:-5] + link[-4:]
    else:
        new_link = link
    return new_link


@register.filter
def bytes_to_megabytes(bytes):

    megabytes = float(bytes) / 1024 / 1024
    return megabytes


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
