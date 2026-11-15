from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.core.management.base import CommandParser

from apps.machines.factories import MachineFactory


class Command(BaseCommand):
    help = "Seed the database with initial machine data"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--count", type=int, default=1, help="Number of machines to create"
        )

    def handle(self, *args, **options):
        count = options["count"]

        if count < 1:
            msg = "--count must be at least 1."
            raise CommandError(msg)

        self.stdout.write(self.style.SUCCESS(f"■ Seeding {count} machines..."))

        try:
            MachineFactory.create_batch(count)
        except Exception as exc:
            msg = f"■ Failed to seed machines: {exc}"
            raise CommandError(msg) from exc

        self.stdout.write(
            self.style.SUCCESS(f"■ Successfully seeded {options['count']} machines.")
        )
