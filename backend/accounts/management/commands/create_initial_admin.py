import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model, authenticate


class Command(BaseCommand):
    help = "Create or synchronize the initial Django superuser."

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    "Initial admin credentials are not configured. Skipping."
                )
            )
            return

        User = get_user_model()

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email or ""},
        )

        user.email = email or ""
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()

        authenticated_user = authenticate(
            username=username,
            password=password,
        )

        self.stdout.write(
            self.style.WARNING(
                f"ADMIN CHECK: username={user.username!r}, "
                f"is_active={user.is_active}, "
                f"is_staff={user.is_staff}, "
                f"is_superuser={user.is_superuser}, "
                f"password_matches={user.check_password(password)}, "
                f"authenticate_success={authenticated_user is not None}"
            )
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Initial admin '{username}' created successfully."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Initial admin '{username}' password synchronized successfully."
                )
            )
