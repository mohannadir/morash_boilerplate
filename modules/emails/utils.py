from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition, Bcc, Cc

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
from typing import Union
import os
import mimetypes
import base64


from django.urls import reverse
from django.template.loader import get_template
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.http import HttpRequest
from django.contrib.staticfiles import finders
from django.conf import settings
from django.core.exceptions import SuspiciousFileOperation
from django.utils.translation import gettext as _

from modules.authentication.tokens import account_activation_token
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model

def send_user_forgot_password_email(user: get_user_model, current_domain: str | None = None) -> bool:
    """ Send forgot password email to user.

        The forgot password email contains a link to the password reset page, which is used to reset the user's password.
        To determine the correct reset link, the current domain is required. This can be passed as a parameter,
        or by default it will be taken from the PLATFORM_URL setting in the Django settings file.
        
        :param user: User object to send forgot password email to.
        :type user: User
        :param current_domain: Domain to use in the reset link. If not provided, the PLATFORM_URL setting will be used.
        :type current_domain: str
        :return: True if email is sent successfully, False otherwise.
        :rtype: bool
    """
    
    if not current_domain:
        current_domain = settings.PLATFORM_URL

    reset_token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    relative_url = reverse('authentication:reset_password', kwargs={'uidb64': uid, 'token': reset_token})
    reset_link = f'{current_domain}{relative_url}'
    
    data = {
        'heading' : _('Reset your password'),
        'subheading' : _('Forgot your password?'),
        'content' : _('Click the button below to reset your password.'),
        'buttons' : [
            {
                'text' : _('Reset password'),
                'url' : reset_link
            }
        ]
    }

    subject = _('Reset your password')
    return send_email_from_base_template(user.email, subject, data)

def send_user_activation_email(user: get_user_model, current_domain: str | None = None) -> bool:
    """ Send activation email to user.

        The activation email contains a link to the activation page, which is used to activate the user's account.
        To determine the correct activation link, the current domain is required. This can be passed as a parameter,
        or by default it will be taken from the PLATFORM_URL setting in the Django settings file.
        
        :param user: User object to send activation email to.
        :type user: User
        :param current_domain: Domain to use in the activation link. If not provided, the PLATFORM_URL setting will be used.
        :type current_domain: str
        :return: True if email is sent successfully, False otherwise.
        :rtype: bool
    """
    
    if not current_domain:
        current_domain = settings.PLATFORM_URL

    activation_token = account_activation_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    relative_url = reverse('authentication:activate_user', kwargs={'uidb64': uid, 'token': activation_token})
    activation_link = f'{current_domain}{relative_url}'
    
    data = {
        'heading' : _('Activate your account'),
        'subheading' : _('Welcome!'),
        'content' : _('Click the button below to activate your account.'),
        'buttons' : [
            {
                'text' : _('Activate account'),
                'url' : activation_link
            }
        ]
    }

    subject = _('Activate your account')
    return send_email_from_base_template(user.email, subject, data)

def send_email_from_base_template(to_emails: Union[list, str], subject: str, template_data, attachments: list = None, cc_emails: Union[list, str] = None, bcc_emails: Union[list, str] = None, remove_attachments_after_send: bool = False) -> bool:
    """ Send email using a base template as the email content. 
    
        :param to_emails: List of email addresses OR single email address to send email to.
        :type to_emails: list or str
        :param subject: Subject of the email.
        :type subject: str
        :param template_data: Data to be passed to the base template.
        :type template_data: dict
        :param attachments: List of file paths to attach to the email.
        :type attachments: list
        :param cc_emails: List of email addresses OR single email address to send email to.
        :type cc_emails: list or str
        :param bcc_emails: List of email addresses OR single email address to send email to.
        :type bcc_emails: list or str
        :param remove_attachments_after_send: Whether to remove the attachments after the email is sent.
        :type remove_attachments_after_send: bool
        :return: True if email is sent successfully, False otherwise.
        :rtype: bool
    """

    # Template data should contain the following
    # heading: str
    # subheading: str
    # content: str
    # buttons: list of dictionaries with keys text and url

    # Add platform config to template data
    template_data['PLATFORM_NAME'] = settings.PLATFORM_NAME

    html_content = get_template('emails/base.html').render(template_data)
    return send_email(to_emails, subject, html_content, attachments, cc_emails, bcc_emails, remove_attachments_after_send)

def send_email_from_template(to_emails: Union[list, str], subject: str, template_path: str, template_data: dict, attachments: list = None, cc_emails: Union[list, str] = None, bcc_emails: Union[list, str] = None, remove_attachments_after_send: bool = False) -> bool:
    """ Send email using a HTML template as the email content. 
    
        :param to_emails: List of email addresses OR single email address to send email to.
        :type to_emails: list or str
        :param subject: Subject of the email.
        :type subject: str
        :param template_path: Path to the HTML template (starting from the templates folder)
        :type template_path: str
        :param template_data: Data to be passed to the HTML template.
        :type template_data: dict
        :param attachments: List of file paths to attach to the email.
        :type attachments: list
        :param cc_emails: List of email addresses OR single email address to send email to.
        :type cc_emails: list or str
        :param bcc_emails: List of email addresses OR single email address to send email to.
        :type bcc_emails: list or str
        :param remove_attachments_after_send: Whether to remove the attachments after the email is sent.
        :type remove_attachments_after_send: bool
        :return: True if email is sent successfully, False otherwise.
        :rtype: bool
    """
    
    html_content = get_template(template_path).render(template_data)
    return send_email(to_emails, subject, html_content, attachments, cc_emails, bcc_emails, remove_attachments_after_send)

def send_email(to_emails: Union[list, str], subject: str, html_content: str, attachments: list = None, cc_emails: Union[list, str] = None, bcc_emails: Union[list, str] = None, remove_attachments_after_send: bool = False) -> bool:
    """ Send email, either with SMTP or SendGrid depending on the CONFIG setting.
        This will add a new task to the task queue, which will send the email asynchronously.

        :param to_emails: List of email addresses OR single email address to send email to.
        :type to_emails: list or str
        :param subject: Subject of the email.
        :type subject: str
        :param html_content: HTML content of the email.
        :type html_content: str
        :param attachments: List of file paths to attach to the email.
        :type attachments: list
        :param cc_emails: List of email addresses OR single email address to send email to.
        :type cc_emails: list or str
        :param bcc_emails: List of email addresses OR single email address to send email to.
        :type bcc_emails: list or str
        :param remove_attachments_after_send: Whether to remove the attachments after the email is sent.
        :type remove_attachments_after_send: bool
        :return: True if email is sent successfully, False otherwise.
        :rtype: bool
    """
    
    from modules.emails.tasks import async_send_email_with_smtp, async_send_email_with_sendgrid
    if settings.EMAIL_PROVIDER == 'sendgrid':
        if settings.EMAIL_USE_TASK_QUEUE:
            return async_send_email_with_sendgrid(to_emails, subject, html_content, attachments, cc_emails, bcc_emails, remove_attachments_after_send)
        else:
            return send_email_with_sendgrid(to_emails, subject, html_content, attachments, cc_emails, bcc_emails, remove_attachments_after_send)
    else:
        if settings.EMAIL_USE_TASK_QUEUE:
            return async_send_email_with_smtp(to_emails, subject, html_content, attachments, cc_emails, bcc_emails, remove_attachments_after_send)
        else:
            return send_email_with_smtp(to_emails, subject, html_content, attachments, cc_emails, bcc_emails, remove_attachments_after_send)

def send_email_with_smtp(to_emails: Union[list, str], subject: str, html_content: str, attachments: list = None, cc_emails: Union[list, str] = None, bcc_emails: Union[list, str] = None, remove_attachments_after_send: bool = False) -> bool:
    """ Send email using SMTP.

        :param to_emails: List of email addresses OR single email address to send email to.
        :type to_emails: list or str
        :param subject: Subject of the email.
        :type subject: str
        :param html_content: HTML content of the email.
        :type html_content: str
        :param attachments: List of file paths to attach to the email.
        :type attachments: list
        :param cc_emails: List of email addresses OR single email address to send email to.
        :type cc_emails: list or str
        :param bcc_emails: List of email addresses OR single email address to send email to.
        :type bcc_emails: list or str
        :param remove_attachments_after_send: Whether to remove the attachments after the email is sent.
        :type remove_attachments_after_send: bool
        :return: True if email is sent successfully, False otherwise.
        :rtype: bool
    """
    
    FROM_EMAIL = settings.EMAIL_HOST_USER
    HOST = settings.EMAIL_HOST
    PORT = settings.EMAIL_PORT
    EMAIL_USER = settings.EMAIL_HOST_USER
    EMAIL_PASSWORD = settings.EMAIL_HOST_PASSWORD
    USE_TLS = settings.EMAIL_USE_TLS
    attachment_paths = []
    
    to_emails = [to_emails] if isinstance(to_emails, str) else to_emails
    cc_emails = [cc_emails] if isinstance(cc_emails, str) else cc_emails
    bcc_emails = [bcc_emails] if isinstance(bcc_emails, str) else bcc_emails
    
    cc_emails = [] if cc_emails is None else cc_emails
    bcc_emails = [] if bcc_emails is None else bcc_emails
    all_emails = to_emails + cc_emails + bcc_emails
    
    message = MIMEMultipart()
    message['From'] = FROM_EMAIL
    message['Date'] = formatdate(localtime=True)
    message['Subject'] = subject
    
    message.attach(MIMEText(html_content, 'html'))
    
    if cc_emails:
        message['Cc'] = COMMASPACE.join(cc_emails)
        to_emails.extend(cc_emails)
    
    if bcc_emails:
        message['Bcc'] = COMMASPACE.join(bcc_emails)
    
    message['To'] = COMMASPACE.join(to_emails)
    
    if attachments:
        for attachment in attachments:
            
            # Search in static files first
            # If not found, search in absolute path
            # If not found, raise error
            try:
                attachment_path = finders.find(attachment)
            except SuspiciousFileOperation: # File not found in static files
                attachment_path = None
            
            if not attachment_path:
                if not os.path.exists(attachment):
                    raise FileNotFoundError(f'Attachment {attachment} not found.')
                else:
                    attachment_path = attachment

            file_name = attachment.split('/')[-1]

            part = MIMEBase('application', "octet-stream")
            with open(attachment_path, 'rb') as f:
                part.set_payload(f.read())
            
            # Add attachment path to list, so we can remove it after the email is sent if needed
            attachment_paths.append(attachment_path)
            
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="{}"'.format(file_name))
            message.attach(part)
    
    try:
        smtp_server = smtplib.SMTP(HOST, PORT)
        
        if USE_TLS:
            smtp_server.starttls()
        
        smtp_server.login(EMAIL_USER, EMAIL_PASSWORD)
        smtp_server.sendmail(FROM_EMAIL, all_emails, message.as_string())
        smtp_server.close()
        
        if remove_attachments_after_send and attachments:
            for attachment_path in attachment_paths:
                os.remove(attachment_path)
                
        return True
    except Exception as e:
        if remove_attachments_after_send and attachments:
            for attachment_path in attachment_paths:
                os.remove(attachment_path)
                
        return False

def send_email_with_sendgrid(to_emails: Union[list, str], subject: str, html_content: str, attachments: list = None, cc_emails: Union[list, str] = None, bcc_emails: Union[list, str] = None, remove_attachments_after_send: bool = False) -> bool:
    """ Send email using SendGrid API. 

        :param to_emails: List of email addresses OR single email address to send email to.
        :type to_emails: list or str
        :param subject: Subject of the email.
        :type subject: str
        :param html_content: HTML content of the email.
        :type html_content: str
        :param attachments: List of file paths to attach to the email.
        :type attachments: list
        :param cc_emails: List of email addresses OR single email address to send email to.
        :type cc_emails: list or str
        :param bcc_emails: List of email addresses OR single email address to send email to.
        :type bcc_emails: list or str
        :param remove_attachments_after_send: Whether to remove the attachments after the email is sent.
        :return: True if email is sent successfully, False otherwise.
        :rtype: bool
    """
    
    FROM_EMAIL = settings.EMAIL_HOST_USER
    SENDGRID_API_KEY = settings.SENDGRID_API_KEY
    attachment_paths = []
    
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_emails,
        subject=subject,
        html_content=html_content
    )

    if cc_emails:
        if isinstance(cc_emails, str):
            cc_emails = [cc_emails]
        
        for cc_email in cc_emails:
            message.add_cc(Cc(cc_email))
    
    if bcc_emails:
        if isinstance(bcc_emails, str):
            bcc_emails = [bcc_emails]
        
        for bcc_email in bcc_emails:
            message.add_bcc(Bcc(bcc_email))
    
    if attachments:
        for attachment in attachments:

            # Search in static files first
            # If not found, search in absolute path
            # If not found, raise error
            try:
                attachment_path = finders.find(attachment)
            except SuspiciousFileOperation: # File not found in static files
                attachment_path = None
            
            if not attachment_path:
                if not os.path.exists(attachment):
                    raise FileNotFoundError(f'Attachment {attachment} not found.')
                else:
                    attachment_path = attachment

            
            file_name = attachment.split('/')[-1]

            with open(attachment_path, 'rb') as f:
                data = f.read()
                f.close()
            
            # Add attachment path to list, so we can remove it after the email is sent if needed
            attachment_paths.append(attachment_path)
            
            mimetype = mimetypes.guess_type(attachment_path)[0]
            if not mimetype:
                mimetype = 'application/octet-stream'
            
            encoded_file = base64.b64encode(data).decode()
            email_attachment = Attachment(
                FileContent(encoded_file),
                FileName(file_name),
                FileType(mimetype),
                Disposition('attachment')
            )
            message.add_attachment(email_attachment)
    
    try:
        client = SendGridAPIClient(SENDGRID_API_KEY)
        response = client.send(message)
        
        if remove_attachments_after_send and attachments:
            for attachment_path in attachment_paths:
                os.remove(attachment_path)

        if response.status_code == 202:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        
        return False