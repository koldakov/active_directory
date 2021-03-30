from django.test import TestCase
from active_directory.models import Settings


class SettingsTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_user_principal_name(self):
        username = 'username@example.com'
        username_outdated = 'example.com\\username'
        username_wrong = 'username'

        self.assertEqual(Settings.get_user_principal_name(username), username)
        self.assertEqual(Settings.get_user_principal_name(username_outdated), username)
        self.assertEqual(Settings.get_user_principal_name(None), None)
        self.assertEqual(Settings.get_user_principal_name(username_wrong), None)

    def test_get_search_base(self):
        username = 'username@example.com'
        search_base = 'dc=example,dc=com'

        #self.assertEqual(Settings.get_search_base(username), search_base)
