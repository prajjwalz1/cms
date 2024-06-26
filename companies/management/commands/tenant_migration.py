# myapp/management/commands/migrate_tenants.py
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django_tenants.utils import get_tenant_model, get_public_schema_name

class Command(BaseCommand):
    help = "Migrate all tenants"

    def handle(self, *args, **options):
        TenantModel = get_tenant_model()
        tenants = TenantModel.objects.exclude(schema_name=get_public_schema_name())

        # First, apply migrations to the public schema
        self.stdout.write("Migrating public schema")
        call_command('migrate', schema_name=get_public_schema_name())

        # Now, apply migrations to each tenant
        for tenant in tenants:
            self.stdout.write(f"Migrating tenant {tenant.schema_name}")
            call_command('migrate', schema_name=tenant.schema_name)

        self.stdout.write(self.style.SUCCESS('Successfully applied migrations to all tenants'))
