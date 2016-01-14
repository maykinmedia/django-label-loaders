from djchoices import DjangoChoices, ChoiceItem


class SiteChoice(ChoiceItem):
    def __init__(self, *args, **kwargs):
        self.site_id = kwargs.pop('site_id', None)
        super(SiteChoice, self).__init__(*args, **kwargs)


class SiteLabels(DjangoChoices):

    @classmethod
    def label_from_site(cls, site):
        """
        Get the label used in the codebase from the site object passed in.

        The possible site names are limited by SITELABELS. So, if we have the
        value of the site name, we can retrieve the associated choices label. By
        default, the label of a choice is the name of the attribute (nudge and
        eindhoven in this case).
        """
        try:
            return cls.values[site.name]
        except KeyError:
            return cls.values[site.domain]
