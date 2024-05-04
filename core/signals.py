from django.core.mail import send_mail
from django.template.loader import render_to_string
from accounts.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Officer  # Import your Officer model


@receiver(post_save, sender=Officer)
def activate_officer(sender, instance, created, **kwargs):
    if instance.status == "Active" and not created:
        # Officer's status changed to Active
        # Generate username based on first name and last name
        username = instance.email
        email = instance.email

        # Check if user with the officer's email already exists
        user_exists = User.objects.filter(email=email).exists()

        if not user_exists:
            # Generate a stronger random password
   

            password = "123Office"

            try:
                # Create user with username and password
                user = User.objects.create_user(
                    username=username, password=password, email=email, is_admin=True
                )
                instance.user = user
                # Send email to officer
                subject = "Your account has been activated"
                message = render_to_string(
                    "activation_email.html",
                    {
                        "username": username,
                        "password": password,
                    },
                )
                send_mail(
                    subject, message, "noreply@example.com", [email]
                )  # Replace with your sender email
            except Exception as e:
                # Handle any errors during user creation or email sending
                print(f"Error: {e}")
