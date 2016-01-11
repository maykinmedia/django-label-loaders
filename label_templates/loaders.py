"""
Wrapper class that takes a list of template loaders as an argument and attempts
to find a label-specific template first, while falling back to the generic
template.
"""
import os

from django.conf import settings
from django.contrib.sites.models import Site
from django.template.base import Template, TemplateDoesNotExist
from django.template.loaders.base import Loader as BaseLoader

# TODO: subclass from cached loader?


class Loader(BaseLoader):
    is_usable = True

    def __init__(self, engine, loaders):
        self.template_cache = {}
        self.find_template_cache = {}
        self.loaders = engine.get_template_loaders(loaders)
        super(Loader, self).__init__(engine)

    def find_template(self, names, dirs=None):
        """
        Helper method. Lookup the template :param name: in all the configured loaders.
        """
        for loader in self.loaders:
            for name in names:
                try:
                    template, display_name = loader(name, dirs)
                except TemplateDoesNotExist:
                    pass
                else:
                    origin = self.engine.make_origin(display_name, loader, name, dirs)
                    return template, origin
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
                template = Template(template, origin, template_name, self.engine)
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
