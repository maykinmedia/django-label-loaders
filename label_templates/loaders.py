"""
Wrapper class that takes a list of template loaders as an argument and attempts
to find a label-specific template first, while falling back to the generic
template.
"""
import os

from django.conf import settings
from django.contrib.sites.models import Site
from django.template.base import TemplateDoesNotExist
from django.template.loader import BaseLoader, get_template_from_string, find_template_loader, make_origin


class Loader(BaseLoader):
    is_usable = True

    def __init__(self, loaders):
        self._loaders = loaders
        self._cached_loaders = []

    @property
    def loaders(self):
        # Resolve loaders on demand to avoid circular imports
        if not self._cached_loaders:
            # Set self._cached_loaders atomically. Otherwise, another thread
            # could see an incomplete list. See #17303.
            cached_loaders = []
            for loader in self._loaders:
                cached_loaders.append(find_template_loader(loader))
            self._cached_loaders = cached_loaders
        return self._cached_loaders

    def find_template(self, names, dirs=None):
        for loader in self.loaders:
            for name in names:
                try:
                    template, display_name = loader(name, dirs)
                    return (template, make_origin(display_name, loader, name, dirs))
                except TemplateDoesNotExist:
                    pass
        raise TemplateDoesNotExist(', '.join(names))

    def load_template(self, template_name, template_dirs=None):
        site = Site.objects.get_current()
        label = settings.SITELABELS.label_from_site(site)

        # put the prefixed template in front of the possible templates
        templates = [
            os.path.join(label, template_name),
            template_name
        ]
        template, origin = self.find_template(templates, template_dirs)
        if not hasattr(template, 'render'):
            try:
                template = get_template_from_string(template, origin, template_name)
            except TemplateDoesNotExist:
                # If compiling the template we found raises TemplateDoesNotExist,
                # back off to returning the source and display name for the template
                # we were asked to load. This allows for correct identification (later)
                # of the actual template that does not exist.
                return template, origin
        return template, None

    def load_template_source(self, template_name, template_dirs=None):
        """
        Returns a tuple containing the source and origin for the given template
        name.

        Dispatch this to the underlying loaders.
        """
        for loader in self.loaders:
            try:
                return loader.load_template_source(template_name, template_dirs=template_dirs)
            except TemplateDoesNotExist:
                pass
        return TemplateDoesNotExist(template_name)
