from typing import Union
from modules.emails.utils import send_email_with_smtp, send_email_with_sendgrid

from huey.contrib.djhuey import task

DEFAULT_RETRY_COUNT = 3 # How many times to retry the task before giving up
DEFAULT_RETRY_DELAY = 60 # How many seconds to wait between retries

@task(retries=DEFAULT_RETRY_COUNT, retry_delay=DEFAULT_RETRY_DELAY)
def async_send_email_with_smtp(to_emails: Union[list, str], subject: str, html_content: str, attachments: list = None, cc_emails: Union[list, str] = None, bcc_emails: Union[list, str] = None, remove_attachments_after_send: bool = False) -> bool:
    """ (Task queue) Send an email using the SMTP protocol. """
    
    return send_email_with_smtp(to_emails, subject, html_content, attachments, cc_emails, bcc_emails, remove_attachments_after_send)

@task(retries=DEFAULT_RETRY_COUNT, retry_delay=DEFAULT_RETRY_DELAY)
def async_send_email_with_sendgrid(to_emails: Union[list, str], subject: str, html_content: str, attachments: list = None, cc_emails: Union[list, str] = None, bcc_emails: Union[list, str] = None, remove_attachments_after_send: bool = False) -> bool:
    """ (Task queue) Send an email using the SendGrid API. """
    
    return send_email_with_sendgrid(to_emails, subject, html_content, attachments, cc_emails, bcc_emails, remove_attachments_after_send)