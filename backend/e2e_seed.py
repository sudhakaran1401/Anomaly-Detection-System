import os

import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "Anomaly_Detection.settings",
)

django.setup()

from django.contrib.auth import get_user_model


USERNAME = "e2e_user"
EMAIL = "e2e.user@example.com"
PASSWORD = "Test@12345"


def seed_e2e_user():
    User = get_user_model()

    user, created = User.objects.get_or_create(
        username=USERNAME,
        defaults={
            "email": EMAIL,
        },
    )

    user.email = EMAIL
    user.set_password(PASSWORD)
    user.is_active = True
    user.save()

    if created:
        print(f"E2E user created: {USERNAME}")
    else:
        print(f"E2E user updated: {USERNAME}")

    print(f"E2E username: {USERNAME}")
    print(f"E2E password: {PASSWORD}")


if __name__ == "__main__":
    seed_e2e_user()