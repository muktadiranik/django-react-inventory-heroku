from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


def user_created(sender, **kwargs):
    if kwargs["created"]:
        user = kwargs["instance"]
        send_mail(
            subject="Thank you for your interest!",
            message="We hope you find what you're looking for and that you enjoy your stay.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False
        )


post_save.connect(receiver=user_created, sender=User)
