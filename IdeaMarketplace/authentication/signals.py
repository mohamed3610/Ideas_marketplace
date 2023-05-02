from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group

from .models import Employee

@receiver(post_save, sender=Employee)
def assign_employee_to_groups(sender, instance, created, **kwargs):
    if created:
        if instance.department == 'HR':
            group = Group.objects.get(name='HR')
            instance.groups.add(group)
        elif instance.department == 'Marketing':
            group = Group.objects.get(name='Marketing')
            instance.groups.add(group)
