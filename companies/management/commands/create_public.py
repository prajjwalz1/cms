from django.core.management.base import BaseCommand
from companies.models import Client, Domain
from datetime import date

class Command(BaseCommand):
    help = 'Create or update the public tenant and its domains'

    def handle(self, *args, **kwargs):
        tenant, created = Client.objects.update_or_create(
            schema_name='public',
            defaults={
                'name': 'Schemas Inc.',
                'paid_until': date(2016, 12, 5),
                'on_trial': False
            }
        )

        domains = ['127.0.0.1']
        for domain_name in domains:
            domain, created = Domain.objects.update_or_create(
                domain=domain_name,
                tenant=tenant,
                defaults={
                    'is_primary': True
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully created or updated public tenant and domains'))
