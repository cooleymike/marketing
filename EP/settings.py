import environ
import os
from pathlib import Path



env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

AUTH_USER_MODEL = "core.Employee"

LOGIN_URL = '/signin/'

# SESSION_COOKIE_DOMAIN = '.marketing.hopto.org'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-fct@82ed^em^in4_n0egg@lx6&qun1g1b4rsc53y((g77atntd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['http://marketing.hopto.org/']



# Application definition

INSTALLED_APPS = [
    #my apps

    
    #django appps (checks these in sequence, make sure all apps are listed
    # here in order of importance
    'django.contrib.admin',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'accounts',
    'django.contrib.sites',

]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('SMTP_GMAIL_ADDRESS')  # your Gmail address
EMAIL_HOST_PASSWORD = env('SMTP_GMAIL_PASSWORD') # not your real password!
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'EP.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'EP.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite32',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, '../static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend'
)
from django_auth_ldap.config import LDAPSearch, PosixGroupType
import ldap

AUTH_LDAP_SERVER_URI = 'ldap://localhost'
AUTH_LDAP_BIND_DN = 'cn=admin,dc=example,dc=org'
AUTH_LDAP_BIND_PASSWORD = 'adminpassword'

AUTH_LDAP_USER_SEARCH = LDAPSearch(
   "ou=marketing,dc=example,dc=org", ldap.SCOPE_SUBTREE, "(uid=%(user)s)"
)
AUTH_LDAP_FIND_GROUP_PERMS = True
# AUTH_LDAP_MIRROR_GROUPS = True
AUTH_LDAP_GROUP_TYPE = PosixGroupType(name_attr='cn')
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
                             'cn=admin,dc=example,dc=org',
                             ldap.SCOPE_SUBTREE,
                             '(objectClass=groupOfNames)'
)
AUTH_LDAP_DENY_GROUP = "cn=blocked_users,dc=example,dc=org"

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
#google
GOOGLE_CLIENT_ID = ('661675223391-rqe1191gcv19q6g6i89s0vi8md51v5qt.apps'
                    '.googleusercontent.com')
GOOGLE_CLIENT_SECRET = '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'
#facebook
SOCIAL_AUTH_FACEBOOK_KEY = '460827666572910'
SOCIAL_AUTH_FACEBOOK_SECRET = 'b17adee16d805838649aaad9dac0031d'
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'APP': {
            'client_id':GOOGLE_CLIENT_ID,
            'secret': GOOGLE_CLIENT_SECRET,
        },
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
    },
    'facebook': {
            'METHOD': 'oauth2',  # Set to 'js_sdk' to use the Facebook connect SDK
            'SDK_URL': '//connect.facebook.net/{locale}/sdk.js',
            # 'SCOPE': ['email', 'public_profile'],
            'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
            'INIT_PARAMS': {'cookie': True},
            'FIELDS': [
                'id',
                'first_name',
                'last_name',
                'middle_name',
                'name',
                'name_format',
                'picture',
                'short_name'
            ],
            'EXCHANGE_TOKEN': True,
            'LOCALE_FUNC': 'path.to.callable',
            'VERIFIED_EMAIL': False,
            'VERSION': 'v13.0',
            'GRAPH_API_URL': 'https://graph.facebook.com/v13.0',
        }

}


