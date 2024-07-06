from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from .models import SalarySlip
from cms.models import Manpower
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import SalarySlip, MonthsalaryRecord, wageAdjustment

@receiver(pre_save, sender=MonthsalaryRecord)
def update_wage_adjustment(sender, instance, **kwargs):
    if instance.status == 'paid':
        for salary_slip in instance.select_salary_slip.all():
            manpower_instance = salary_slip.employee
            paying_amount = salary_slip.paying_amount
            net_salary = manpower_instance.salary_amount
            print(paying_amount,net_salary)
            if paying_amount < net_salary:
                difference = net_salary - paying_amount 
                wage_adjustment, created = wageAdjustment.objects.get_or_create(
                    employee=manpower_instance,
                )
                wage_adjustment.advance -= difference
                if wage_adjustment.advance < 0:
                    wage_adjustment.credit+= abs(wage_adjustment.advance)
                    wage_adjustment.advance=0
                wage_adjustment.save()
            elif paying_amount > net_salary:
                difference = paying_amount - net_salary
                wage_adjustment, created = wageAdjustment.objects.get_or_create(
                    employee=manpower_instance,
                )
                
                wage_adjustment.credit -= difference

                if wage_adjustment.credit < 0:
                    wage_adjustment.advance += abs(wage_adjustment.credit)
                    wage_adjustment.credit=0
                    
                wage_adjustment.save()

@receiver(post_save, sender=SalarySlip)
def update_adjustable(sender, instance, created, **kwargs):
    if created:
        if instance.employee:
            manpower_instance = instance.employee

            # Update adjustable field based on conditions
            if manpower_instance.salary_amount < instance.paid_amount:
                instance.adjustable = instance.paid_amount - manpower_instance.salary_amount
                instance.save()

            # Create or update wageAdjustment record for advances
            wage_adjustment, created = wageAdjustment.objects.get_or_create(
                employee=manpower_instance,
                date=instance.date_recorded,
            )
            if created:
                wage_adjustment.advance = instance.adjustable  # Set advance amount
            else:
                wage_adjustment.advance += instance.adjustable  # Add to existing advance
            wage_adjustment.save()

            # Create or update MonthsalaryRecord
            month_record, created = MonthsalaryRecord.objects.get_or_create(
                month=instance.month,
                year=instance.year,
            )
            month_record.select_salary_slip.add(instance)  # Add salary slip to MonthsalaryRecord
            month_record.save()
