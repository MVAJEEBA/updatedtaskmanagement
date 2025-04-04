from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from taskapp.models import CustomUser  # Assuming 'ManageUser' is your custom User model

class Command(BaseCommand):
    help = 'Create user roles and assign permissions'

    def handle(self, *args, **kwargs):
        # Create roles
        user_group, created = Group.objects.get_or_create(name='employee')
        manager_group, created = Group.objects.get_or_create(name='manager')
        admin_group, created = Group.objects.get_or_create(name='Admin')

        # Assign permissions
        publish_permission = Permission.objects.get(codename='can_publish_document')
        archive_permission = Permission.objects.get(codename='can_archive_document')
        
        # Add permissions to groups
        user_group.permissions.add(publish_permission)
        manager_group.permissions.add(archive_permission)
        admin_group.permissions.add(publish_permission, archive_permission)

        self.stdout.write(self.style.SUCCESS('Roles and permissions have been set up successfully!'))

        # Loop through users and assign them to their appropriate groups based on roles
        users = CustomUser.objects.all()

        for user in users:
            # Determine user role and assign them to the corresponding group
            if user.role == 'employee':
                user_group = Group.objects.get(name='employee')
            elif user.role == 'manager':
                user_group = Group.objects.get(name='manager')
            elif user.role == 'admin':
                user_group = Group.objects.get(name='admin')
            else:
                continue  # If no role is defined, skip the user

            # Add user to their respective group
            user.groups.add(user_group)

        self.stdout.write(self.style.SUCCESS('Roles assigned to users based on their roles!'))
