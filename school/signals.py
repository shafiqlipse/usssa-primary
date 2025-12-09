from django.db.models.signals import pre_save, post_save
from accounts.models import User
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from .models import *


@receiver(post_save, sender=School)
def create_school_admin(sender, instance, created, **kwargs):
    if created:
        # Generate school admin credentials
        school_admin_email = instance.email
        school_games_email = instance.gemail
        school_admin_username = instance.email
        school_admin_password = (
            "123Pass"  # You might want to generate a more secure password
        )

        # Create a school admin user and associate it with the school
        hashed_password = make_password(school_admin_password)
        school_admin_user = User.objects.create(
            username=school_admin_username,
            email=school_admin_email,
            password=hashed_password,
            is_school=True,
        )
        instance.user = school_admin_user

        instance.save()
        html_message = render_to_string("core/email.html")
        plain_message = strip_tags(html_message)
        subject = "Your School Admin Account Details"
        message = plain_message
        from_email = "noreply@usssaonline.com"  # Replace with your email
        recipient_list = [school_admin_user.email,school_games_email]

        send_mail(subject, message, from_email, recipient_list)



@receiver(pre_save, sender=Payment)
def update_athlete_status_on_payment_completion(sender, instance, **kwargs):
    if not instance.pk:
        # Payment is being created (initial status is PENDING), no need to update athletes
        return

    # Get the previous state of the payment from the database
    previous = Payment.objects.get(pk=instance.pk)

    # Check if status changed from PENDING to COMPLETED
    if previous.status == 'PENDING' and instance.status == 'COMPLETED':
        # Update all related athletes to ACTIVE
        instance.athletes.update(status='ACTIVE')


