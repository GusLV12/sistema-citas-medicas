from django.core.management.base import BaseCommand

from scheduling.services import create_due_reminders


class Command(BaseCommand):
    help = "Crea recordatorios internos de citas a 24 h y 2 h; es seguro ejecutarlo cada 15 minutos."

    def handle(self, *args, **options):
        created = create_due_reminders()
        self.stdout.write(self.style.SUCCESS(f"Recordatorios creados: {created}"))
