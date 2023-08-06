from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from backend.settings import SUPPORT_PHONE_NUMBER, SUPPORT_EMAIL_ADDRESS


class Mailer:
    """ The Mailer class holds helper functions for sending template emails """

    @classmethod
    def send_email(cls, to_emails, subject, template, context, bcc=None, attachments=None):
        email_context = {
            "support_phone_number": SUPPORT_PHONE_NUMBER,
            "support_email_address": SUPPORT_EMAIL_ADDRESS,
        }
        email_context.update(context)

        email_text = render_to_string(f"email/{template}.txt", email_context)
        email_html = render_to_string(f"email/{template}.html", email_context)

        message = EmailMultiAlternatives(
            subject=subject,
            body=email_text,
            from_email="MetLife Legal Plans <support@legalplans.com>",
            to=to_emails,
            bcc=bcc,
        )

        message.attach_alternative(email_html, "text/html")
        if attachments:
            for item in attachments:
                message.attach(*item)

        try:
            message.send()
            return True
        # TODO: handle specific exceptions
        except Exception as e:
            # TODO: report exception
            print(e, vars(e))
            return False

    @classmethod
    def send_account_notice(cls, user, subject, text):
        return cls.send_email(
            [user.email],
            f"Account Notice: {subject}",
            "mlp_transactional_email",
            {"user": user, "notice": text,},
        )
