from django.apps import AppConfig

from django.utils.translation import ugettext_lazy as _


class GrapherConfig(AppConfig):
    name = 'apps.grapher'
    verbose_name = _('grapher')

    def ready(self):
        import apps.grapher.signals
