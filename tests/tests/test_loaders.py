from __future__ import unicode_literals

from django.contrib.sites.models import Site
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.test import override_settings, TestCase


class LoaderTests(TestCase):

    def setUp(self):
        Site.objects.get_or_create(id=2, domain='example2.com', name='Site 2')

    def test_load_app_generic_template(self):
        """
        Test that 'base.html' from 'app' loads.
        """
        template = get_template('base.html')
        self.assertEqual(template.render(), 'Fallback template\n')

    def test_load_app_specific_template(self):
        """
        Test that the 'specific.html' template is loaded from the
        app, in favour of the 'generic' version.

        Also assert that the generic 'base.html' is used to extend.
        """
        template = get_template('specific.html')
        self.assertEqual(template.render(), 'Fallback templateApp label specific\n')

    @override_settings(SITE_ID=2)
    def test_load_different_site(self):
        """
        Test that template loading falls through to the generic version if
        it doesn'\t exist for a certain site.
        """
        template = get_template('specific.html')
        self.assertEqual(template.render(), 'Generic version\n')

    def test_template_does_not_exist(self):
        with self.assertRaises(TemplateDoesNotExist) as cm:
            get_template('non-existant.html')

        self.assertEqual(cm.exception.args, ('non-existant.html',))

    def test_filesystem_loader(self):
        """
        Tests that second configured sub-loader works as intended.
        """
        template = get_template('filesystem.html')
        self.assertEqual(template.render(), 'filesystem\n')

    def test_try_all_loaders_first(self):
        """
        Tests that first all loaders are tried for the label-specific template,
        then all loaders are tried for the generic template.

        `templates/site/order.html` does not exist, so
        `app/templates/site/order.html` must be retrieved before
        `templates/order.html`.
        """
        template = get_template('order.html')
        self.assertEqual(template.render(), 'app order\n')

        with self.settings(SITE_ID=2):
            template = get_template('order.html')
            self.assertEqual(template.render(), 'generic order\n')
