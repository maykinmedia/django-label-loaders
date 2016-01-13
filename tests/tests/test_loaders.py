from __future__ import unicode_literals

from django.contrib.sites.models import Site
from django.template.loader import get_template
from django.test import override_settings, SimpleTestCase


class LoaderTests(SimpleTestCase):

    def setUp(self):
        Site.objects.get_or_create(id=2, domain='example2.com', name='Site 2')

    def test_load_app_generic_template(self):
        """
        Test that 'base.html' from 'app' loads.
        """
        template = get_template('base.html')
        self.assertEqual(template.template.name, 'base.html')

    def test_load_app_specific_template(self):
        """
        Test that the 'specific.html' template is loaded from the
        app, in favour of the 'generic' version.

        Also assert that the generic 'base.html' is used to extend.
        """
        template = get_template('specific.html')
        self.assertEqual(template.template.name, 'site/specific.html')
        self.assertEqual(template.render(), 'Fallback template\n')

    @override_settings(SITE_ID=2)
    def test_load_different_site(self):
        """
        Test that template loading falls through to the generic version if
        it doesn'\t exist for a certain site.
        """
        template = get_template('specific.html')
        self.assertEqual(template.render(), 'Generic version\n')
