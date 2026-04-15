"""Core adapters module.

This module provides custom account adapters for django-allauth,
including CustomAccountAdapter to control signup behavior and email handling.
"""

import logging

from allauth.account.adapter import DefaultAccountAdapter

from django.conf import settings
from django.http import HttpRequest

logger = logging.getLogger("core")


class CustomAccountAdapter(DefaultAccountAdapter):
    """Adapter to disable allauth new signups.

    Used at equilang/settings.py with key ACCOUNT_ADAPTER

    https://django-allauth.readthedocs.io/en/latest/advanced.html#custom-redirects
    """

    def is_open_for_signup(self, request: HttpRequest) -> bool:
        """Check whether or not the site is open for signups.

        Next to simply returning True/False you can also intervene the
        regular flow by raising an ImmediateHttpResponse
        """
        return False

    # def get_email_subject_prefix(self, context):
    #     """Completely disable the automatic [Site] prefix."""
    #     return ""

    # def render_mail(self, template_prefix, email, context, headers=None):
    #     msg = super().render_mail(template_prefix, email, context, headers)

    #     # Force the subject via headers (some SMTP backends respect this)
    #     if headers is None:
    #         headers = {}
    #     headers["X-Subject"] = msg.subject  # Explicitly set the subject
    #     msg.extra_headers = headers

    #     return msg

    # def render_mail(self, template_prefix, email, context, headers=None):
    #     """Complete email rendering override.

    #     1. Doesn't add any automatic prefixes
    #     2. Uses the exact subject from the template
    #     3. Preserves all other email functionality
    #     """
    #     # Get the raw subject from template
    #     subject = render_to_string(
    #         f"{template_prefix}_subject.txt",
    #         context
    #     ).strip()
    #     logger.debug("Subject: %s", subject)
    #     # Create the email message
    #     msg = EmailMultiAlternatives(
    #         subject=subject,
    #         body=render_to_string(f'{template_prefix}_message.txt', context),
    #         from_email=self.get_from_email(),
    #         to=[email],
    #         headers=headers or {}
    #     )

    #     # Add HTML version if available
    #     try:
    #         msg.attach_alternative(
    #             render_to_string(f"{template_prefix}_message.html", context),
    #             "text/html"
    #         )
    #     except Exception as e:
    #         logger.debug("No HTML template for %s: %s", template_prefix, e)
    #     email_details = {
    #         "subject": msg.subject,
    #         "from": msg.from_email,
    #         "to": msg.to,
    #         "cc": msg.cc,
    #         "bcc": msg.bcc,
    #         "headers": dict(msg.extra_headers),
    #         "body": msg.body,
    #         "content_subtype": msg.content_subtype,
    #         "attachments": [
    #             {
    #                 "filename": attachment[0],
    #                 "type": attachment[1],
    #                 "size": (
    #                     len(attachment[2])
    #                     if isinstance(attachment[2], (str, bytes))
    #                     else "binary"
    #                 ),
    #             }
    #             for attachment in msg.attachments
    #         ],
    #         "alternatives": [
    #             {
    #                 "content": f"{alt[0][:100]}..." if len(alt[0]) > 100 else alt[0],
    #                 "mimetype": alt[1],
    #             }
    #             for alt in msg.alternatives
    #         ],
    #     }
    #     logger.debug("Complete email message:\n%s",
    #     json.dumps(email_details, indent=2, ensure_ascii=False))
    #     # Log the complete email message
    #     logger.debug("Complete email message:\nSubject: %s\nFrom: %s\nTo: %s\nHeaders: %s\nBody: %s\nAttachments: %d",
    #         msg.subject,
    #         msg.from_email,
    #         msg.to,
    #         msg.extra_headers,
    #         msg.body,
    #         len(msg.attachments))
    #     return msg

    def get_from_email(self) -> str:
        """Ensure consistent from email address."""
        return settings.DEFAULT_FROM_EMAIL


# class CustomAccountAdapter(DefaultAccountAdapter):

# def get_email_subject_prefix(self, context):
#     """Completely override to return empty string - prevents [site] prefix."""
#     return ""

# def format_email_subject(self, subject):
#     """Remove any site name prefix like [localhost:8000] from the subject."""
#     subject = super().format_email_subject(subject)
#     print(subject)
#     # Remove things like [localhost], [example.com], [My Site], etc.
#     subject = re.sub(r"^\s*\[.*?\]\s*", "", subject)

#     # Optional: remove redundant leading characters like " - " or ":"
#     subject = re.sub(r"^[-:\s]+", "", subject)
#     print(subject)
#     return subject.strip()
# def format_email_subject(self, subject):
#     """Completely bypass all subject formatting."""
#     return "Acervo Invest - Redefinir sua senha"

# def render_mail(self, template_prefix, email, context, headers=None):
#     """Override render_mail to completely control email generation."""
#     # Add current site to context if not present
#     if 'current_site' not in context:
#         context['current_site'] = Site.objects.get_current()

#     subject = render_to_string(
#         f"{template_prefix}_subject.txt",
#         context,
#         request=context.get("request")
#     ).strip()

#     # Clean the subject aggressively
#     subject = self.format_email_subject(subject)

#     message = render_to_string(
#         f'{template_prefix}_message.txt',
#         context,
#         request=context.get('request')
#     )

#     html_message = None
#     try:
#         html_message = render_to_string(
#             f"{template_prefix}_message.html",
#             context,
#             request=context.get('request')
#         )
#     except:
#         pass

#     # Create headers dict if not provided
#     if headers is None:
#         headers = {}

#     # Ensure no site prefix is added by explicitly setting headers
#     headers.update({
#         'Reply-To': self.get_from_email(),
#     })

#     msg = EmailMultiAlternatives(
#         subject=subject,
#         body=message,
#         from_email=self.get_from_email(),
#         to=[email],
#         headers=headers
#     )

#     if html_message:
#         msg.attach_alternative(html_message, "text/html")

#     return msg

# def render_mail(self, template_prefix, email, context, headers=None):
#     msg = super().render_mail(template_prefix, email, context, headers)
#     # Completely replace the subject with your clean version
#     msg.subject = "Acervo Invest - Redefinir sua senha"
#     return msg

# def send_mail(self, template_prefix, email, context):
#     """Override send_mail to use our render_mail and prevent Django from adding prefixes."""
#     msg = self.render_mail(template_prefix, email, context)

#     # Double-check the subject before sending
#     msg.subject = self.format_email_subject(msg.subject)

#     try:
#         msg.send()
#         logger.info("Sent account email to %s using template '%s'", email, template_prefix)
#     except Exception as e:
#         logger.exception("Failed to send account email to %", email)

# def get_from_email(self):
#     """Ensure consistent from email."""
#     return getattr(settings, "DEFAULT_FROM_EMAIL", settings.EMAIL_HOST_USER)
