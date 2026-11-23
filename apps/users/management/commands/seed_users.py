from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.core.management.base import CommandParser
from rolepermissions.roles import assign_role

from apps.users.factories import UserFactory
from config.roles import Admin
from config.roles import Operator


class Command(BaseCommand):
    help = "Seed the database with test users"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--count",
            type=int,
            default=1,
            help="Number of users to create",
        )
        parser.add_argument(
            "--role",
            type=str,
            default="Operator",
            choices=["Admin", "Operator"],
            help="Role to assign to users",
        )

    def handle(self, *args, **options):
        count = options["count"]
        role = options["role"]

        if count < 1:
            msg = "--count must be at least 1."
            raise CommandError(msg)

        self.stdout.write(self.style.SUCCESS(f"■ Seeding {count} {role} users..."))

        try:
            users = UserFactory.create_batch(count)

            role_class = Admin if role == "Admin" else Operator
            for user in users:
                # Set password to last_name (matching your pattern)
                user.set_password(user.last_name)
                user.save()
                assign_role(user, role_class)

        except Exception as exc:
            msg = f"■ Failed to seed users: {exc}"
            raise CommandError(msg) from exc

        self.stdout.write(
            self.style.SUCCESS(f"■ Successfully seeded {count} {role} users.")
        )
