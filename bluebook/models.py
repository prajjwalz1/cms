from django.db import models

# Create your models here.
from django.db import models

class VehicleTaxInsurance(models.Model):
    province = models.CharField(max_length=50)
    vehicle_type = models.CharField(max_length=50)
    engine_cc = models.CharField(max_length=50, null=True, blank=True)
    tax_rate_2081 = models.FloatField()
    insurance_premium = models.FloatField(null=True, blank=True)
    personal_accident_premium = models.FloatField(null=True, blank=True)
    total_premium = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.province} - {self.vehicle_type} - {self.engine_cc}"
