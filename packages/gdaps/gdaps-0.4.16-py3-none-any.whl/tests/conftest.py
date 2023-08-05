import os

import django
from django.core import management


def pytest_configure(config):
    from django.conf import settings

    settings.configure(
        SECRET_KEY="test",
        BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        DATABASES={
            "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
        },
        INSTALLED_APPS=["gdaps", "tests.plugins.plugin1"],
        PLUGIN1={"OVERRIDE": 20},
    )

    django.setup()
