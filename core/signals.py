# from django.contrib.auth.models import Group
# from django_auth_ldap.backend import populate_user
#
#
# @populate_user.connect #decorator coming from object populate_user
# def add_user_to_group(sender, user=None, ldap_user=None, **kwargs):
#     # Replace 'MyGroup' with the name of the group you want users to join
#     group_name = 'Employee'
#
#     group, created = Group.objects.get_or_create(name=group_name)
#
#     if not user.groups.filter(name=group_name).exists():
#         user.groups.add(group)
