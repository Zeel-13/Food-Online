from django.contrib.sites.shortcuts import get_current_site

from django.template.loader import render_to_string

from django.utils.http import urlsafe_base64_encode

from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage

from django.contrib.auth.tokens import default_token_generator
def detectUser(user):
    if user.role==1:
        redirectUrl='vendorDashboard'
    elif user.role==2:
        redirectUrl='customerDashboard' 
    elif user.role==None and user.is_superadmin:
        redirectUrl='/admin'
    return redirectUrl

def send_verefication_email(request,user):
    current_site = get_current_site(request)
    mail_subject = 'Activate your account'
    message = render_to_string('accounts/emails/account_verification_email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email=user.email
    mail=EmailMessage(mail_subject,message,to=[to_email])
    mail.send() 

def send_password_reset_email(request,user):
    current_site = get_current_site(request)
    mail_subject = 'Reset your password'
    message = render_to_string('accounts/emails/reset_password_email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email=user.email
    mail=EmailMessage(mail_subject,message,to=[to_email])
    mail.send() 

def send_notification_email(mail_subject,mail_template,context):
    message=render_to_string(mail_template,context)
    to_email=context['user'].email
    mail=EmailMessage(mail_subject,message,to=[to_email])
    mail.send()