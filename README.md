# Module for working with active directory. Includes Authentication Using LDAP

This modules created to working with active directory. Includes module to Authentication Using LDAP.

This version is written and tested on Python 3.8.5; and Django 3.1.5; and ldap3 2.9.

## Installation

Install the ldap3 package with pip:
```console
$ pip install ldap3=2.9
```

To use Django Authentication backend add ```'ldap_backend.backend.LDAPBackend'``` to ```AUTHENTICATION_BACKENDS``` in settings.py.
You should get something like this:
```python
AUTHENTICATION_BACKENDS = [
    'django_auth_ldap.backend.LDAPBackend',
    'ldap_backend.backend.LDAPBackend'
]
```

To use templates add os.path.join(BASE_DIR, 'active_directory.templates') to 'DIRS' in 'TEMPLATES'

## Configuration Example

You can get settings through settings.py:
```python
SETTINGS_ACTIVE_DIRECTORY = [
    {
        username: 'username',
        password: 'password',
        domain: 'domain',
        ssl: False,
        port: 389
    }
]
```

Or through "Settings" (preferred). Do migration, add record to table.
If you want to use only 'Authentication Using LDAP' you don't need to fill 'username' and 'password' - this fields will be get from auth form.

## Conclusion

This modules should be used not only to Authentication Using LDAP it is something more. It could be used to synchronize AD values, writing your own management commands and so on.

If you have a bug or feature request contact me.
