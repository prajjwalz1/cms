from django.db import models
from cms.mixins import *
from cms.models import Manpower
# Create your models here.
from django.core.exceptions import ValidationError
from cms.models import SupplierModel
class wageAdjustment(models.Model):
    employee = models.ForeignKey(Manpower, on_delete=models.DO_NOTHING)
    advance = models.IntegerField(default=0)
    credit = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.employee.name

    @staticmethod
    def total_advance(employee_id):
        return wageAdjustment.objects.filter(employee_id=employee_id).aggregate(total_advance=models.Sum('advance'))['total_advance'] or 0

    @staticmethod
    def total_credit(employee_id):
        return wageAdjustment.objects.filter(employee_id=employee_id).aggregate(total_credit=models.Sum('credit'))['total_credit'] or 0

    @staticmethod
    def net_advance(employee_id):
        total_advance = wageAdjustment.total_advance(employee_id)
        total_credit = wageAdjustment.total_credit(employee_id)
        return total_advance - total_credit

class SalarySlip(DateTimeModel):
    employee=models.ForeignKey(Manpower,on_delete=models.DO_NOTHING)
    paying_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_recorded = models.DateField(default=timezone.now)

    def __str__(self):
        return self.employee.name


def validate_bs_year(value):
    if value < 2000 or value > 2100:
        raise ValidationError(f'{value} is not a valid Bikram Sambat year. Year must be between 2000 and 2100.')

class MonthsalaryRecord(models.Model):
    MONTH_CHOICES = [
        ('baisakh', 'Baisakh'),
        ('jestha', 'Jestha'),
        ('ashar', 'Ashar'),
        ('shrawan', 'Shrawan'),
        ('bhadra', 'Bhadra'),
        ('ashwin', 'Ashwin'),
        ('kartik', 'Kartik'),
        ('mangsir', 'Mangsir'),
        ('poush', 'Poush'),
        ('magh', 'Magh'),
        ('falgun', 'Falgun'),
        ('chaitra', 'Chaitra'),
    ]
    
    month = models.CharField(max_length=10, choices=MONTH_CHOICES)
    year = models.PositiveIntegerField(validators=[validate_bs_year],default=2081) 
    select_salary_slip = models.ManyToManyField('SalarySlip')
    status = models.CharField(
        max_length=10,
        choices=(
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('paid', 'Paid')
        ),
        default='pending'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['month', 'year'], name='unique_month_year')
        ]

    def __str__(self) -> str:
        return f'{self.year} {self.month}'
    



class CreditRecord(models.Model):
    supplier = models.ForeignKey(SupplierModel, on_delete=models.CASCADE)
    credit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    credit_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Credit of {self.supplier.name}"
