from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from mailing.models import Mailing, Recipient, Message
from users.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='Managers')
        
        # Define permissions for managers
        permissions = [
            'view_any_mailing',
            'set_mailing_status',
            'view_any_recipient',
            'view_any_message',
            'view_user', # Built-in
        ]
        
        for perm_code in permissions:
            try:
                # Try to find custom and built-in permissions
                perm = Permission.objects.filter(codename=perm_code).first()
                if perm:
                    group.permissions.add(perm)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Could not add permission {perm_code}: {e}'))
        
        self.stdout.write(self.style.SUCCESS('Successfully created Managers group and assigned permissions'))
