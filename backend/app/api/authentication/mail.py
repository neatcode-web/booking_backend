from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_password_reset_mail(email, token) :
    url = settings.FRONTEND + "guest/reset_password/" + str(token)
    msg_html = render_to_string('password-reset.html', {'url': url})
    send_mail(
        'Password Reset',
        '',
        settings.EMAIL_SENDER,
        [email],
        html_message=msg_html,
    )
