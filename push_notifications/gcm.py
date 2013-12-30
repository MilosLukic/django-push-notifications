"""
Google Cloud Messaging
Previously known as C2DM
Documentation is available on the Android Developer website:
https://developer.android.com/google/gcm/index.html
"""

import json
import requests

from django.core.exceptions import ImproperlyConfigured
from . import NotificationError
from .settings import PUSH_NOTIFICATIONS_SETTINGS as SETTINGS

from push_notifications.models import GCMDevice


class GCMError(NotificationError):
    pass


def _chunks(l, n):
    """
    Yield successive chunks from list \a l with a minimum size \a n
    """
    for i in range(0, len(l), n):
        yield l[i:i + n]


def _gcm_send(data, content_type='application/json'):
    key = SETTINGS.get("GCM_API_KEY")
    if not key:
        raise ImproperlyConfigured(
            'You need to set PUSH_NOTIFICATIONS_SETTINGS["GCM_API_KEY"] to send messages through GCM.')

    headers = {
        "UserAgent": "GCM-Server",
        "Content-Type": content_type,
        "Authorization": "key=%s" % key,
    }

    registration_ids = data.get('registration_ids')
    data = json.dumps(data)

    response = requests.post(url=SETTINGS["GCM_POST_URL"],
                             data=data,
                             headers=headers)

    return process_response_for_errors(registration_ids, response.json())


def process_response_for_errors(recipient_list, response):
    results = response.get('results')

    for r in zip(results, recipient_list):
        if r[0].get('error') == 'NotRegistered':
            device = GCMDevice.objects.get(registration_id=r[1])
            device.active = False
            device.save()
        if r[0].get('message_id'):
            if r[0].get('registration_id'):
                device = GCMDevice.objects.get(registration_id=r[1])
                device.registration_id = r[0].get('registration_id')
                device.save()

    return response


def gcm_send_message(registration_id, data, collapse_key=None, time_to_live=None,delay_while_idle=False):
    """
    Sends a GCM notification to a single registration_id.
    This will send the notification as form data.
    If sending multiple notifications, it is more efficient to use
    gcm_send_bulk_message()
    """

    values = {
        "registration_ids": [registration_id,],
        "data": data
    }

    if collapse_key:
        values["collapse_key"] = collapse_key

    if delay_while_idle:
        values["delay_while_idle"] = delay_while_idle

    if time_to_live:
        values["time_to_live"] = time_to_live

    return _gcm_send(values)


def gcm_send_bulk_message(registration_ids, data, collapse_key=None, time_to_live=None, delay_while_idle=False):
    """
    Sends a GCM notification to one or more registration_ids. The registration_ids
    needs to be a list.
    This will send the notification as json data.
    """

    # GCM only allows up to 1000 reg ids per bulk message
    # https://developer.android.com/google/gcm/gcm.html#request
    max_recipients = SETTINGS.get("GCM_MAX_RECIPIENTS")
    if len(registration_ids) > max_recipients:
        ret = []
        for chunk in _chunks(registration_ids, max_recipients):
            ret.append(gcm_send_bulk_message(chunk, data, collapse_key, time_to_live, delay_while_idle))
        return ret

    values = {
        "registration_ids": registration_ids,
        "data": data,
    }

    if collapse_key:
        values["collapse_key"] = collapse_key

    if delay_while_idle:
        values["delay_while_idle"] = delay_while_idle

    if time_to_live:
        values["time_to_live"] = time_to_live

    return _gcm_send(values)
