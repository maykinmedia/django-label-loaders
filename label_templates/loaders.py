"""
Wrapper class that takes a list of template loaders as an argument and attempts
to find a label-specific template first, while falling back to the generic
template.
"""
import os
import warnings

from django.conf import settings
from django.contrib.sites.models import Site
from django.template import TemplateDoesNotExist
from django.template.loaders.base import Loader as BaseLoader
from django.utils.deprecation import RemovedInDjango20Warning


class Loader(BaseLoader):
    is_usable = True

    def __init__(self, engine, loaders):
        self.loaders = engine.get_template_loaders(loaders)
        super(Loader, self).__init__(engine)

    def load_template_source(self, template_name, template_dirs=None):
        """
        Returns a tuple containing the source and origin for the given template
        name.

        Dispatch this to the underlying loaders.
        """
        warnings.warn(
            'The load_template_sources() method is deprecated. Use '
            'get_template() or get_contents() instead.',
            RemovedInDjango20Warning,
        )

        site = Site.objects.get_current()
        label = settings.SITELABELS.label_from_site(site)

        # put the prefixed template in front of the possible templates
        names = [os.path.join(label, template_name), template_name]
        for name in names:  # always try to load the label-specific version first, independent from the loader
            for loader in self.loaders:
                try:
                    return loader.load_template_source(name, template_dirs=template_dirs)
                except TemplateDoesNotExist:
                    pass
        raise TemplateDoesNotExist("Tried %s" % ', '.join(names))
