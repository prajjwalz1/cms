from django.core.management.base import BaseCommand
from companies.models import Client, Domain

class Command(BaseCommand):
    help = 'Create the public tenant and its domain'

    def handle(self, *args, **kwargs):
        tenant = Client(schema_name='public2',
                        name='Schemas Inc.',
                        paid_until='2016-12-05',
                        on_trial=False)
        tenant.save()

        domain = Domain()
        domain.domain = 'localhost'  # don't add your port or www here! On a local server, use 'localhost'
        domain.tenant = tenant
        domain.is_primary = True
        domain.save()

        self.stdout.write(self.style.SUCCESS('Successfully created public tenant and domain'))
