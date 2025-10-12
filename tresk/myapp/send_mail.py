from django.core.mail import send_mail
from tresk.settings import DEFAULT_FROM_EMAIL
from django.template.loader import render_to_string
from django.conf import settings


class SendMail:
    @staticmethod
    def send_email_to_client(show, tickets, order):
        
        html_message = render_to_string("send_email.html", {
            "show" : show,
            "tickets" : tickets,
            "order" : order.full_name
        }

        )
        if order:
            subject=f"🎭 Ваш билет заказан"
            message="Ваш билет успешно оформлен."
            send_mail(
                subject=subject,
                message=message,
                from_email=DEFAULT_FROM_EMAIL,
                recipient_list=[order.email],
                html_message=html_message,
                fail_silently=False
            )
