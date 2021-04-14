from active_directory.utils.active_directory import get_users_info_ad
from django.core.management.base import BaseCommand
from ldap3.core.exceptions import LDAPException


class Command(BaseCommand):
    help = 'Get information from active directory by given parameters. Search through all active directory settings'

    def add_arguments(self, parser):
        parser.add_argument(
            '-u',
            '--users',
            nargs='+',
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

        parser.add_argument(
            '-d',
            '--domains',
            nargs='+',
            help='Use definite active directory Settings'
        )

    def handle(self, *args, **options):
        users = options.get('users') or None
        attributes = options.get('attributes') or '*'
        login_username = options.get('login_username')[0] if options.get('login_username') else None
        login_password = options.get('login_password')[0] if options.get('login_password') else None
        domains = options.get('domains') or None

        try:
            users_info = get_users_info_ad(
                login_username=login_username, login_password=login_password,
                users=users, domains=domains, attributes=attributes
            )
        except LDAPException as e:
            return str(e)
        if users_info:
            for user in users_info:
                # TODO Change print to return (pretty view)
                print(user.get('dn'))
            return 0
        else:
            return 'Users not found'

        return '-h/--help'
