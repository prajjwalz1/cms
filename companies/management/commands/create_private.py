# companies/management/commands/create_tenant.py

from django.core.management.base import BaseCommand, CommandError
from companies.models import Client, Domain
from django_tenants.utils import schema_context

class Command(BaseCommand):
    help = 'Create a new tenant with the specified schema name and domain'

    def add_arguments(self, parser):
        parser.add_argument('--schema_name', type=str, help='The schema name for the tenant')
        parser.add_argument('--name', type=str, help='The name of the tenant')
        parser.add_argument('--domain', type=str, help='The domain for the tenant')

    def handle(self, *args, **options):
        schema_name = options['schema_name'] or input('Enter schema name: ')
        name = options['name'] or input('Enter tenant name: ')
        domain = options['domain'] or input('Enter domain: ')

        # Check if the schema name already exists
        if Client.objects.filter(schema_name=schema_name).exists():
            raise CommandError(f'Tenant with schema name "{schema_name}" already exists.')

        # Create the tenant
        tenant = Client(schema_name=schema_name, name=name)
        tenant.save()

        # Create the domain for the tenant
        tenant_domain = Domain(domain=domain, tenant=tenant, is_primary=True)
        tenant_domain.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully created tenant "{name}" with domain "{domain}"'))
