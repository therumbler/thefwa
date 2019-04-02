from email.mime.text import MIMEText
import logging
import os
import sys

SENDMAIL = '/usr/sbin/sendmail'
logger = logging.getLogger(__name__)


def send_email(message_string, recipients=['therumbler@gmail.com'], subject='FWA update'):
    if not isinstance(recipients, list):
        recipients = [recipients]

    logger.info('sending email...')
    message = MIMEText(message_string)
    message['Subject'] = subject
    message['From'] = 'no-reply@alpha.irumble.com'
    message['To'] = '; '.join(recipients)

    pipe = os.popen('{} -t -i'.format(SENDMAIL), 'w')
    pipe.write(message.as_string())
    status = pipe.close()
    if status:
        logger.error('Sendmail status: "%s"', status)


def setup_logging(mode=logging.DEBUG):
    """setup stdout logging"""
    root = logging.getLogger()
    root.setLevel(mode)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(pathname)s - %(funcName)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

