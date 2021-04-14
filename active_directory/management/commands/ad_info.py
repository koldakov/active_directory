from django.core.management.base import BaseCommand
from active_directory.utils.active_directory import get_users_info_ad


class Command(BaseCommand):
    help = 'Get information from active directory by given parameters. Search through all active directory settings'

    def add_arguments(self, parser):
        parser.add_argument(
            '-u',
            '--users',
            nargs='*',
            help='Get users information from active directory. Specify without domain controller'
        )

        parser.add_argument(
            '-a',
            '--attributes',
            nargs='*',
            help='What attributes to search in active directory'
        )

        parser.add_argument(
            '-lu',
            '--login-username',
            nargs=1,
            help='Active directory username login'
        )

        parser.add_argument(
            '-lp',
            '--login-password',
            nargs=1,
            help='Active directory password login'
        )

    def handle(self, *args, **options):
        users = options.get('users') or None
        attributes = options.get('attributes') or '*'
        login_username = options.get('login_username')[0] if options.get('login_username') else None
        login_password = options.get('login_password')[0] if options.get('login_password') else None

        users_info = get_users_info_ad(
            login_username=login_username, login_password=login_password,
            users=users, attributes=attributes
        )
        if users_info:
            for user in users_info:
                # TODO change print to return (pretty view)
                print(user.get('dn'))
            return 0
        else:
            return 'Users not found'

        return '-h/--help'
