
from django.core.mail import EmailMultiAlternatives


class SendEmail:
    @staticmethod
    def send_email(data):
        email = EmailMultiAlternatives(
            subject=data['subject'],
            text_content=data['text_content'],
            from_email=data['from_email'],
            to_email=[data['to_email']],
        )
        email.attach_alternative(data['html_content'], "text/html")
        email.send(fail_silently=False)


