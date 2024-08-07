from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from dashboard.models import School, school_official
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.utils.html import strip_tags
from django.template.loader import render_to_string


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


# @receiver(post_save, sender=school_official)
# def update_school_admin_credentials(sender, instance, created, **kwargs):
#     if created and instance.school.user and instance.school.school.count() == 1:
#         # Update school admin user's email and username only for the first school official
#         school_admin_user = instance.school.user
#         school_admin_user.email = instance.email
#         school_admin_user.username = (
#             instance.email
#         )  # You might want to customize this logic
#         school_admin_user.save()
# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
# from .models import School

@receiver(post_save, sender=School)
def set_school_active(sender, instance, **kwargs):
    if instance.status == 'inactive':
        instance.status = 'active'
        instance.save()
