from django.core.management.base import BaseCommand

from apps_dir.accounts.models import User


class Command(BaseCommand):
    help = "This will create the initial super user"

    def handle(self, *args, **options):
        """
        Create the super user
        :param args:
        :param options:
        :return:
        """
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'emmanuelt2009@gmail.com', 'admin', user_type=1)
            print("superuser created")
        else:
            print("superuser already exists")
