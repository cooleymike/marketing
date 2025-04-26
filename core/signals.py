from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver


from core.models import Employee


@receiver(post_save, sender=Employee)
def add_user_to_group(sender, instance, created, **kwargs):
    if created:
       group, _ = Group.objects.get_or_create(name='Marketing')  # replace 'DefaultGroup' with your group name
       instance.groups.add(group)

