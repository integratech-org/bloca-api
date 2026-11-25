import random

from allauth.account.models import EmailAddress
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.core.management.base import CommandParser
from django.db import transaction
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

        self.stdout.write(self.style.SUCCESS(f"■ Seeding {count} users..."))

        roles = [Admin, Operator, SystemAdmin]

        try:
            with transaction.atomic():
                users = UserFactory.create_batch(count)

                for user in users:
                    user.set_password(user.last_name)
                    user.save()

                    EmailAddress.objects.create(
                        user=user,
                        email=user.email,
                        verified=True,
                        primary=True,
                    )

                    assign_role(user, random.choice(roles))  # noqa: S311

        except Exception as exc:
            msg = f"■ Failed to seed users: {exc}"
            raise CommandError(msg) from exc

        self.stdout.write(self.style.SUCCESS(f"■ Successfully seeded {count} users."))
