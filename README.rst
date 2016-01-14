======================
Django Label Templates
======================

A custom template loader for multi-site set-ups.


.. image:: https://travis-ci.org/maykinmedia/django-label-loaders.svg?branch=master
    :target: https://travis-ci.org/maykinmedia/django-label-loaders


.. image:: https://codecov.io/github/maykinmedia/django-label-loaders/coverage.svg?branch=master
    :target: https://codecov.io/github/maykinmedia/django-label-loaders?branch=master


.. image:: https://coveralls.io/repos/maykinmedia/django-label-loaders/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/maykinmedia/django-label-loaders?branch=master


.. image:: https://img.shields.io/pypi/v/django-label-templates.svg
  :target: https://pypi.python.org/pypi/django-label-templates


This is intended for users of ``django.contrib.sites`` for multi-site cases
where a different site can have different templates, not only a different
styling.

The custom template loaders will try to find a template for the currently
active site, and fall back on a generic template.


Installation
============

Install with pip::

    pip install django-label-templates


Configuration
=============

Installed apps
--------------

Make sure that ``django.contrib.sites`` is in your ``INSTALLED_APPS``.


Specify template loaders
------------------------

You also need to enable the loader in the settings, similar to Django's
cached template loader. The loader takes an iterable (list or tuple) of
loaders to find the templates. Example - and probably most used - set-up:


.. code-block:: python

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            # APP_DIRS must be False if you specify the loaders yourself
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

If you wish, this template loader can also be wrapped in other loaders,
like ``django.template.loaders.cached.Loader``.


Configure the site labels
-------------------------

For the final step, one extra custom settings is required: ``SITELABELS``.

.. code-block:: python

    # the import is safe and does NOT depend on django.conf.settings
    from label_templates.sites import SiteLabels, SiteChoice

    class SITELABELS(SiteLabels):
        site = SiteChoice('example.com', site_id=1)
        site2 = SiteChoice('example2.com', site_id=2)


This settings is used to look up the label-prefix for the templates. The site
with ``ID=1`` will resolve to a subfolder ``site/``, so to load the template
``example.html``, the loader will try to find ``site/example.html`` first, and
failing that, will try to just load ``example.html``.

For the site with ``ID=2``, the prefix ``site2`` is used.

.. note:: To find the matching site, the loader tries to get the label for the
   ``SiteChoice`` based on ``django.contrib.sites.models.Site.name``, with a
   fallback to ``domain``. So, for the first argument of ``SiteChoice``, it's
   safest to enter the ``Site.name`` value.


Limitations
===========

Since the ``{% extends %}`` tag uses the same loader configuration, you can not
let a label-specific template inherit from a generic template with the same
name.

A workaround is the following structure::

    templates/
    ├── mylabel/
    |   └── base.html  # extends _base.html and overrides stuff
    ├── _base.html
    └── base.html  # extends _base.html, overrides nothing


Versions supported
==================

This library is tested against Django 1.8 and 1.9. The corresponding Python
versions for the Django versions apply. Consult ``tox.ini`` for an up to date
build matrix.
