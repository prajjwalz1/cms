from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django_tenants.utils import schema_context
from companies.models import Client

class Command(BaseCommand):
    help = 'Create a superuser for a specified tenant'

    def add_arguments(self, parser):
        parser.add_argument('schema_name', type=str, help='The schema name of the tenant')
        parser.add_argument('username', type=str, help='The desired username for the superuser')
        parser.add_argument('email', type=str, help='The email address of the superuser')
        parser.add_argument('password', type=str, help='The password for the superuser')

    def handle(self, *args, **kwargs):
        schema_name = kwargs['schema_name']
        username = kwargs['username']
        email = kwargs['email']
        password = kwargs['password']

        try:
            tenant = Client.objects.get(schema_name=schema_name)
        except Client.DoesNotExist:
            raise CommandError(f'Tenant with schema name "{schema_name}" does not exist')

        with schema_context(schema_name):
            if User.objects.filter(username=username).exists():
                raise CommandError(f'A user with username "{username}" already exists in tenant "{schema_name}"')
            
            user = User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created for tenant "{schema_name}"'))
