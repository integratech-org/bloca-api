import random

from allauth.account.models import EmailAddress
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.core.management.base import CommandParser
from rolepermissions.roles import assign_role

from apps.users.factories import UserFactory
from config.roles import Admin
from config.roles import Operator
from config.roles import SystemAdmin


class Command(BaseCommand):
    help = "Seed the database with test users"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--count",
            type=int,
            default=1,
            help="Number of users to create",
        )

    def handle(self, *args, **options):
        count = options["count"]

        if count < 1:
            msg = "--count must be at least 1."
            raise CommandError(msg)

        self.stdout.write(
            self.style.SUCCESS(f"■ Seeding {count} users with random roles...")
        )

        try:
            users = UserFactory.create_batch(count)

            roles = [Admin, Operator, SystemAdmin]
            for user in users:
                # Set password to last_name (matching your pattern)
                user.set_password(user.last_name)
                user.save()

                # Create verified email
                EmailAddress.objects.create(
                    user=user,
                    email=user.email,
                    verified=True,
                    primary=True,
                )

                # Assign random role
                role_class = random.choice(roles)  # noqa: S311
                assign_role(user, role_class)

        except Exception as exc:
            msg = f"■ Failed to seed users: {exc}"
            raise CommandError(msg) from exc

        self.stdout.write(
            self.style.SUCCESS(
                f"■ Successfully seeded {count} users with random roles."
            )
        )
