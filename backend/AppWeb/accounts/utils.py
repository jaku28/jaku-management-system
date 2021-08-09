"""Accounts app utils."""

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template import loader
from django.utils.translation import ugettext as _


def send_welcome_email(request, user):
    """Send a welcome email to a recently register user."""
    # activate(user.profile.language)
    current_site = get_current_site(request)
    site_name = current_site.name
    domain = current_site.domain

    context = {
        'user': user,
        'domain': domain,
        'protocol': 'https' if request.is_secure() else 'http',
    }

    from_email = f'{site_name} Team <no-reply@{domain}>'
    to_email = user.email
    subject = _('Welcome to AppWeb!')

    template = loader.get_template('accounts/email/welcome.html')
    message = template.render(context)

    return send_mail(subject, '', from_email, [to_email], fail_silently=True, html_message=message)
