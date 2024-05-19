import threading

from django.template.loader import render_to_string
from django.core.mail import send_mail

from django.conf import settings


class AccountsEmailNotification:
    def _send_email_in_thread(self, subject: str, message: str, from_email: str, recipient_list: list[str]) -> None:
        threading.Thread(
            target=send_mail,
            args=(subject, message, from_email, recipient_list),
            kwargs={'fail_silently': False, 'html_message': message}
        ).start()

    def send_activation_email(self, email: str, full_name: str, activation_url: str) -> None:
        subject = "Welcome to Our Site!"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        context = {
            'full_name': full_name,
            'activation_url': activation_url
        }

        message = render_to_string('registration/registration_email.html', context)
        self._send_email_in_thread(subject, message, from_email, recipient_list)
