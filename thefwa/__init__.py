import json
import logging
import time
import urllib.request as request
from urllib.error import HTTPError

from .models import Case

logger = logging.getLogger(__name__)


def fetch_json(url, retry=False):
    """make a GET request to JSON endpoint"""
    
    try:
        logger.debug('fetching url "%s"...', url)
        resp = request.urlopen(url)
    except HTTPError as ex:
        logger.error('HTTPError %s', str(ex))
        if not retry:
            return None
        logger.debug('waiting for a bit then will try again...')
        time.sleep(5)
        return fetch_json(url)

    return json.load(resp)

def fetch_cases():
    url = 'https://thefwa.com/api/live/cases'
    cases = fetch_json(url)
    return cases


def fetch_updates():
    url = 'https://thefwa.com/api/live/updates'
    updates = fetch_json(url)
    if not updates:
        return None
    with open('./cache/updates.json', 'w') as f:
        f.write(json.dumps(updates, indent=2))
    return updates['cases']

