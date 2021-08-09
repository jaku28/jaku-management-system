from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site

from django.core import mail
from django.core.mail.backends.smtp import EmailBackend

class email_util:
    def _init_(self):
        self.email_from = ""
    
    #Send a simple email
    def send_simple_email(self, to, subject, content_message):
        send_mail(subject, content_message, "", [to])

    #Check for email seetings
    def _check_mail_settings(self):
        connection = mail.get_connection()
        if isinstance(connection, EmailBackend):
            connection.open()
    
    #Send an email to the entrepreneur with the response to their request
    def send_email_html(self, request, profile, is_accepted):
        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain
        user = profile.user
        if is_accepted:
            pwd = profile.temp_pwd
            context = {
                'user': user,
                'pwd': pwd,
                'domain': domain,
                'protocol': 'https' if request.is_secure() else 'http',
            }
            subject = "¡Has sido aprobado para tu registro!"
            html_message = render_to_string('entrepreneur_registry/request_entrepreneur/acceptance_email.html', context)
        
        else:
            context = {
                'user': user,
                'domain': domain,
                'protocol': 'https' if request.is_secure() else 'http',
            }
            subject = "Lo sentimos, no has sido aprobado."
            html_message = render_to_string('entrepreneur_registry/request_entrepreneur/rejected_email.html', context)
        
        from_email = 'jaku.emprende@gmail.com'
        plain_message = strip_tags(html_message)
        to_email = user.email
        send_mail(subject, plain_message, from_email, [to_email], fail_silently=False, html_message=html_message)

    #Send an email to the entrepreneur with the response to their request
    def send_email_entrepreneur(self, request, profile, project):
        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain
        user = profile.user
        
        context = {
            'user': user,
            'project': project,
            'domain': domain,
            'protocol': 'https' if request.is_secure() else 'http',
        }
        subject = "¡Has sido agregado a un nuevo proyecto!"
        html_message = render_to_string('common/project/request_project/add_email.html', context)
        
        from_email = 'jaku.emprende@gmail.com'
        plain_message = strip_tags(html_message)
        to_email = user.email
        send_mail(subject, plain_message, from_email, [to_email], fail_silently=False, html_message=html_message)

    #Send an email to the mentor when a mentoring is created
    def send_email_mentoring(self, request, mentoring):
        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain
        context = {
                'm': mentoring,
                'domain': domain,
                'protocol': 'https' if request.is_secure() else 'http',
        }
        subject = "¡Tienes una nueva mentoria!"
        html_message = render_to_string('mentoring/creation_email.html', context)
        from_email = 'jaku.emprende@gmail.com'
        plain_message = strip_tags(html_message)
        to_email = mentoring.mentor.user.email
        send_mail(subject, plain_message, from_email, [to_email], fail_silently=False, html_message=html_message)

    #Send an email to the entrepreneur with the result of the first filter
    def send_email_filter(self, request, profile, is_approved):
        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain
        user = profile
        
        if is_approved == '2':
            context = {
                'user': user,
                'domain': domain,
                'protocol': 'https' if request.is_secure() else 'http',
            }
            subject = "¡Tu proyecto ha sido aceptado!"
            html_message = render_to_string('common/call/project_classification/acceptance_email.html', context)
        
        else:
            context = {
                'user': user,
                'domain': domain,
                'protocol': 'https' if request.is_secure() else 'http',
            }
            subject = "Lo sentimos, tu proyecto ha sido rechazado."
            html_message = render_to_string('common/call/project_classification/rejected_email.html', context)
        
        from_email = 'jaku.emprende@gmail.com'
        plain_message = strip_tags(html_message)
        to_email = user.email
        send_mail(subject, plain_message, from_email, [to_email], fail_silently=False, html_message=html_message)

    #Send an email to the entrepreneur with the response to their request
    def send_email_coach(self, request, coach, project):
        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain
        user = coach.user
        
        context = {
            'user': user,
            'project': project,
            'domain': domain,
            'protocol': 'https' if request.is_secure() else 'http',
        }
        subject = "¡Has sido asignado como coach de un nuevo proyecto!"
        html_message = render_to_string('coach_assignment/notify_email.html', context)
        
        from_email = 'jaku.emprende@gmail.com'
        plain_message = strip_tags(html_message)
        to_email = user.email
        send_mail(subject, plain_message, from_email, [to_email], fail_silently=False, html_message=html_message)