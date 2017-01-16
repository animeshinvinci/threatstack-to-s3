'''
Communicate with Threat Stack
'''
import os
import requests
import sys

THREATSTACK_BASE_URL = os.environ.get('THREATSTACK_BASE_URL', 'https://app.threatstack.com/api/v1')
THREATSTACK_API_KEY = os.environ.get('THREATSTACK_API_KEY')

class ThreatStackError(Exception):
    '''
    Base Threat Stack error class.
    '''

class ThreatStackRequestError(ThreatStackError):
    '''
    Error in request to Threat Stack.
    '''

class ThreatStackAPIError(ThreatStackError):
    '''
    Error returned from Threat Stack API.
    '''
    def __init__(self, message, status_code, response=None):
        self.message = message
        self.status_code = status_code
        self.response = response

def is_available():
    '''
    Check connectivity to Threat Stack.

    Returns a failure if cannot connect to Threat Stack API.  This could be
    anything from API credential issues to connection failure.
    '''

    alerts_url = '{}/alerts?count=1'.format(THREATSTACK_BASE_URL)

    try:
        resp = requests.get(
            alerts_url,
            headers={'Authorization': THREATSTACK_API_KEY}
        )
    except requests.exceptions.RequestException as e:
        exc_info = sys.exc_info()
        raise ThreatStackRequestError, ThreatStackRequestError(e), exc_info[2]


    if not resp.ok:
        if 'application/json' in resp.headers.get('Content-Type'):
            raise ThreatStackAPIError(resp.reason, resp.status_code, resp.json())
        else:
            raise ThreatStackAPIError(resp.reason, resp.status_code)

    return True

def get_alert_by_id(alert_id):
    '''
    Retrieve an alert from Threat Stack by alert ID.
    '''
    alerts_url = '{}/alerts/{}'.format(THREATSTACK_BASE_URL, alert_id)

    try:
        resp = requests.get(
            alerts_url,
            headers={'Authorization': THREATSTACK_API_KEY}
        )
    except requests.exceptions.RequestException as e:
        exc_info = sys.exc_info()
        raise ThreatStackRequestError, ThreatStackRequestError(e), exc_info[2]

    if not resp.ok:
        if 'application/json' in resp.headers.get('Content-Type'):
            raise ThreatStackAPIError(resp.reason, resp.status_code, resp.json())
        else:
            raise ThreatStackAPIError(resp.reason, resp.status_code)

    return resp.json()

