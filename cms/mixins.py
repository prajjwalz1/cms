from django.db import models
from django.utils import timezone
from rest_framework.response import Response


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class DateTimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True,editable=False)
    objects = SoftDeleteManager()

    def delete(self, hard=False, *args, **kwargs):
        if hard:
            super(DateTimeModel, self).delete(*args, **kwargs)
        else:
            self.deleted_at = timezone.now()
            super(DateTimeModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class ResponseMixin:
    """
    Handles Both Error and Successfull response
    """

    def handle_error_response(self, error_message, status_code):
        return Response(
            {"success": False, "error": str(error_message)},
            status=status_code,
        )

    def handle_success_response(self, status_code, serialized_data=None, message=None):
        response = {"success": True}
        if serialized_data:
            response["data"] = serialized_data
        else:
            response["data"] = []

        if message:
            response["message"] = message

        return Response(
            response,
            status=status_code,
        )


class GetSingleObjectMixin:
    """
    Fetches single object of given model using PK
    """

    def get_object(self, model_class, pk):
        try:
            return model_class.objects.get(pk=pk), None
        except Exception as e:
            return None, f"Item with id '{pk}' does not exists."
