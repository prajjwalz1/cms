from django.apps import AppConfig


class WorkflowConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'workflow'

    def ready(self):
        # Import your model here to avoid circular import
        from .models import FuelWorkflow
