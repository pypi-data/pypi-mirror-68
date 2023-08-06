import os
from logging import getLogger

from django.conf import settings
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.urls import path
from django.views.generic import TemplateView

logger = getLogger(__file__)

template_name = None
try:
    template_name = get_template(
        os.path.join(settings.PROJECT_NAME, "index.html")
    ).template.name
except TemplateDoesNotExist:
    pass
except TypeError:  # no template found, .name not applicable then
    pass
finally:
    if not template_name:
        template_name = os.path.join("gdaps/index.html")

logger.critical(f"using template {template_name} as Vue entry point loader")

urlpatterns = [
    path("", TemplateView.as_view(template_name=template_name), name="app", )
    # path("", TemplateView.as_view(template_name="gdaps/application.html"), name="app")
]
