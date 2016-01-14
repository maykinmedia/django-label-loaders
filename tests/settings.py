import os

from label_templates.sites import SiteLabels, SiteChoice


PROJECT_DIR = os.path.dirname(__file__)
BASE_DIR = PROJECT_DIR  # setting present in new startproject


SITE_ID = 1


INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'label_templates',
    'tests.app',
]

ROOT_URLCONF = 'tests.urls'

DEBUG = False
SECRET_KEY = 'this-is-really-not-a-secret'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'database.db'),
    }
}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': False,
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'OPTIONS': {
            'loaders': [
                ('label_templates.loaders.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],
        },
    },
]


class SITELABELS(SiteLabels):
    site = SiteChoice('example.com', site_id=1)
    site2 = SiteChoice('example2.com', site_id=2)
