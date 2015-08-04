# Django settings for Macnamer
from settings_import import ADMINS, TIME_ZONE, LANGUAGE_CODE, ALLOWED_HOSTS
import os
import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType, PosixGroupType
# Django settings for macnamer project.


#LDAP CONFIGURATION

# ...connecting to ldap server (local environment uses IP)
AUTH_LDAP_GLOBAL_OPTIONS = {
    ldap.OPT_X_TLS_REQUIRE_CERT: False,
    ldap.OPT_REFERRALS: False
}
AUTH_LDAP_SERVER_URI = "ldap://ldap"

# ...account to enter into ldap server (anonymous is not always allowed)
AUTH_LDAP_BIND_DN = "cn=admin,dc=ldap,dc=reallifechurch,dc=org"
AUTH_LDAP_BIND_PASSWORD = os.environ['LDAP_PASSWORD']

# ...node where to start to search users
AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=people,dc=ldap,dc=reallifechurch,dc=org",
                                   ldap.SCOPE_SUBTREE,  # allow searching from current node to all nodes below
                                   "(uid=%(user)s)"
                                   #"(objectClass=posixAccount)"
                                   #"(objectClass=simpleSecurityObject)"
)

# ...path where to start to search groups
AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=group,dc=ldap,dc=reallifechurch,dc=org",
                                    ldap.SCOPE_SUBTREE,  # allow searching from current node to all nodes below
                                    "(objectClass=posixGroup)"  # type of object
)
AUTH_LDAP_GROUP_TYPE = PosixGroupType(name_attr="cn")  # a posixGroup is identified by the keyword "cn" into ldap server

# ...simple group restrictions
AUTH_LDAP_REQUIRE_GROUP = "cn=macnamer_admin,ou=group,dc=ldap,dc=reallifechurch,dc=org"


# ...populate the Django user from the LDAP directory.
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
    "username": "uid",
    "password": "userPassword",
}

AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    'is_active': 'cn=macnamer_admin,ou=group,dc=ldap,dc=reallifechurch,dc=org',
    'is_staff': 'cn=macnamer_admin,ou=group,dc=ldap,dc=reallifechurch,dc=org',
    'is_superuser': 'cn=macnamer_admin,ou=group,dc=ldap,dc=reallifechurch,dc=org',
}

# Keep ModelBackend around for per-user permissions and maybe a local
# superuser.
AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

import logging
logger = logging.getLogger('django_auth_ldap')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

#End LDAP CONFIGURATION


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_DIR, 'db/macnamer.db'),                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
# deprecated in Django 1.4, but django_wsgiserver still looks for it
# when serving admin media
ADMIN_MEDIA_PREFIX = '/static_admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'site_static'),
)

LOGIN_URL='/login/'
LOGIN_REDIRECT_URL='/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '6%y8=x5(#ufxd*+d+-ohwy0b$5z^cla@7tvl@n55_h_cex0qat'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'macnamer.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'macnamer.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'namer',
    'south',
    'bootstrap_toolkit',
)

#LDAP LOGGING
import logging, logging.handlers
logfile = "/home/app/macnamer/django-ldap-debug.log"
my_logger = logging.getLogger('django_auth_ldap')
my_logger.setLevel(logging.DEBUG)

handler = logging.handlers.RotatingFileHandler(
   logfile, maxBytes=1024 * 500, backupCount=5)
