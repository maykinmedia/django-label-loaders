from django import VERSION


def make_origin(name, template_name, loader, engine, dirs):

    if VERSION < (1, 9):
        return engine.make_origin(name, loader, template_name, dirs)
    else:
        from django.template import Origin
        return Origin(
            name=name,
            template_name=template_name,
            loader=loader,
        )
