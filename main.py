import argparse
import json
import logging
import os
import sys

from thefwa import fetch_cases, fetch_updates
from thefwa.models import Update
from thefwa.utilities import send_email, setup_logging


logger = logging.getLogger(__name__)



def main():
    """let's go!"""
    setup_logging()
    email_recipients = os.getenv('THEFWA_EMAIL_RECIPIENTS')
    if not email_recipients:
        logger.error('env var THEFWA_EMAIL_RECIPIENTS not set')
        sys.exit(1)
    email_recipients = email_recipients.split(',')
    parser = argparse.ArgumentParser()
    parser.add_argument('id', help='the FWA id of the case you want to check')
    args = parser.parse_args()
    try:
        with open('./cache/updates_previous.json') as f:
            updates_previous = json.load(f)
    except FileNotFoundError:
        logger.error('updates_previous.json does not exist')
        updates_previous = []

    updates = fetch_updates()
    if not updates:
        logger.error('ERROR: fetch_updates returned nothing')
        sys.exit(1)

    try:
        update = [u for u in updates if u['id'] == int(args.id)][0]
    except IndexError:
        logger.error('cannot find case id = %s', args.id)
        sys.exit(1)

    try:
        update_previous = [u for u in updates_previous if u['id'] == int(args.id)][0]
    except IndexError:
        logger.error('no previous update')

    inst_new = Update(**update)
    inst_previous = Update(**update_previous)
    if inst_new.hash() != inst_previous.hash():
        logger.info('something changed')
        logger.info('previous = %s', repr(inst_previous))
        logger.info('new = %s', repr(inst_new))
        message_string = f'''
        FWA Case id {args.id} has changed.

        Old: {repr(inst_previous)}
        New: {repr(inst_new)}

        more information here https://thefwa.com/live-judging/
        '''.strip()
        send_email(
            message_string,
            recipients=email_recipients,
            subject=f'Update to FWA Case id {args.id}'
        )
    else:
        logger.info('nothing changed')

    with open('./cache/updates_previous.json', 'w') as f:
        f.write(json.dumps(updates))

    return


if __name__ == '__main__':
    main()

