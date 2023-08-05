.. usage:

Usage
=====

Creating plugins
----------------
If you use git in your project, install the ``gitpython`` module (``pip install gitpython --dev``). ``startplugin`` will determine your git user/email automatically and use it.

Create a plugin using a Django management command:

.. code-block:: bash

    ./manage.py startplugin fooplugin

This command asks a few questions, creates a basic Django app in the plugin path chosen in ``PluginManager.find_plugins()``. It provides useful defaults as well as a setup.py/setup.cfg file.

You now have two choices for this plugin:

* add it statically to ``INSTALLED_APPS``: see `Static plugins <#static-plugins>`_.
* make use of the dynamic loading feature: see `Dynamic plugins <#dynamic-plugins>`_.

Static plugins
^^^^^^^^^^^^^^

In most of the cases, you will ship your application with a few
"standard" plugins that are statically installed. These plugins must be
loaded *after* the ``gdaps`` app.

.. code-block:: python

    # ...

    INSTALLED_APPS = [
        # ... standard Django apps and GDAPS
        "gdaps",

        # put "static" plugins here too:
        "myproject.plugins.fooplugin",
    ]

This plugin app is loaded as usual, but your GDAPS enhanced Django application
can make use of it's GDAPS features.

Dynamic plugins
^^^^^^^^^^^^^^^

By installing a plugin with pip, you can make your application
aware of that plugin too:

.. code:: bash

    pip install -e myproject/plugins/fooplugin

This installs the plugin as python module into the site-packages and
makes it discoverable using setuptools. From this moment on it should be
already registered and loaded after a Django server restart. Of course
this also works when plugins are installed from PyPi, they don't have to
be in the project's ``plugins`` folder. You can conveniently start
developing plugins in there, and later move them to the PyPi repository.


The plugin AppConfig
--------------------

Plugins' AppConfigs must provide an inner class named ``PluginMeta``, or a so named attribute pointing to an external class. For more information see :class:`gdaps.apps.PluginMeta`.

.. _Interfaces:

Interfaces
----------

Plugins can define interfaces, which can then be implemented by other
plugins. The ``startplugin`` command will create a ``<app_name>/api/interfaces.py`` file automatically.
It's not obligatory to put all Interface definitions in that module, but it is a recommended coding style for GDAPS plugins:

.. code-block:: python

    from gdaps import Interface

    @Interface
    class IFooInterface:
        """Documentation of the interface"""

        __service__ = True  # is the default

        def do_something(self):
            pass

Interfaces can have a default Meta class that defines Interface options.
Available options:

.. _service:

__service__
    If ``__service__ = True`` is set (which is the default), then all implementations are
    instantiated directly at loading time, having a full class instance
    availably at any time. Iterations over Interfaces return **instances**:

    .. code-block:: python

        for plugin in IFooInterface:
            plugin.do_something()

..

    If you use ``__service__ = False``, the plugins are not instantiated, and
    iterations over Instances will return **classes**, not instances.
    This may be desired for reducing memory footprint, data classes, or classes that
    just contain static or class methods.

    .. code-block:: python

        for plugin in INonServiceInterface:
            print(plugin.name)  # class attribute
            plugin.classmethod()

            # if you need instances, you have to instantiate the plugin here.
            # this is not recommended.
            p = plugin()
            p.do_something()
..

.. _Implementations:

Implementations
---------------

You can then easily implement this interface in any other file (in this
plugin or in another plugin) by subclassing the interface:

.. code-block:: python

    from myproject.plugins.fooplugin.api.interfaces import IFooInterface

    class OtherPluginClass(IFooInterface):

        def do_something(self):
            print('I did something!')


Using Implementations
---------------------
You can straight-forwardly use implementations that are bound to an interface by iterating over that interface,
anywhere in your code.

.. code-block:: python

    from myproject.plugins.fooplugin.api.interfaces import IFooInterface

    class MyPlugin:

        def foo_method(self):
            for plugin in IFooInterface:
                print plugin.do_domething()

Depending on the `__service__ <#service>`__ Meta flag, iterating over an Interface
returns either a **class** (``__service__ = False``) or an **instance** (``__service__ = True``), which is the default.


Extending Django's URL patterns
-------------------------------

To let your plugin define some URLs that are automatically detected by your Django application, you
have to add some code to your global urls.py file:

.. code-block:: python

    from gdaps.pluginmanager import PluginManager

    urlpatterns =  [
        # add your fixed, non-plugin paths here.
    ]

    # just add this line after the urlpatterns definition:
    urlpatterns += PluginManager.urlpatterns()

GDAPS then loads and imports all available plugins' *urls.py*  files,
collects their ``urlpatterns`` variables and merges them into the global
one.

A typical ``fooplugin/urls.py`` would look like this:

.. code-block:: python

    from . import views

    app_name = "fooplugin"

    urlpatterns =  [
        path("/fooplugin/myurl", views.MyUrlView.as_view()),
    ]

GDAPS lets your plugin create global, root URLs, they are not
namespaced. This is because soms plugins need to create URLS for
frameworks like DRF, etc. Plugins are responsible for their URLs, and
that they don't collide with others.

.. _Settings:

Per-plugin Settings
-------------------

GDAPS allows your application to have own settings for each plugin
easily, which provide defaults, and can be overridden in the global
``settings.py`` file. Look at the example conf.py file (created by
``./manage.py startplugin fooplugin``), and adapt to your needs:

.. code-block:: python

    from django.test.signals import setting_changed
    from gdaps.conf import PluginSettings

    NAMESPACE = "FOOPLUGIN"

    # Optional defaults. Leave empty if not needed.
    DEFAULTS = {
        "MY_SETTING": "somevalue",
        "FOO_PATH": "django.blah.foo",
        "BAR": [
            "baz",
            "buh",
        ],
    }

    # Optional list of settings that are allowed to be in "string import" notation. Leave empty if not needed.
    IMPORT_STRINGS = (
        "FOO_PATH"
    )

    # Optional list of settings that have been removed. Leave empty if not needed.
    REMOVED_SETTINGS = ( "FOO_SETTING" )


    fooplugin_settings = PluginSettings("FOOPLUGIN", None, DEFAULTS, IMPORT_STRINGS)

Detailed explanation:

DEFAULTS
   The ``DEFAULTS`` are, as the name says, a default array of settings. If
   ``fooplugin_setting.BLAH`` is not set by the user in settings.py, this
   default value is used.

IMPORT_STRINGS
   Settings in a *dotted* notation are evaluated, they return not the
   string, but the object they point to. If it does not exist, an
   ``ImportError`` is raised.

REMOVED_SETTINGS
   A list of settings that are forbidden to use. If accessed, an
   ``RuntimeError`` is raised.

   This allows very flexible settings - as dependant plugins can easily
   import the ``fooplugin_settings`` from your ``conf.py``.

   However, the created conf.py file is not needed, so if you don't use
   custom settings at all, just delete the file.


Admin site
----------
GDAPS provides support for the Django admin site. The built-in ``GdapsPlugin`` model automatically
are added to Django's admin site, and can be administered there.

.. note::

    As GdapsPlugin database entries must not be edited directly, they are shown read-only in the admin.
    **Please use the 'syncplugins' management command to
    update the fields from the file system.**
    However, you can enable/disable or hide/show plugins via the admin interface.

If you want to disable the built-in admin site for GDAPS, or provide a custom GDAPS ModelAdmin, you can do this using:

.. code-block:: python

    GDAPS = {
        "ADMIN": False
    }


.. _usage-frontend-support:

Frontend plugins
^^^^^^^^^^^^^^^^

The GDAPS frontend module can be extended via plugins, each providing a pluggable frontend for your Django application. See

Signals
^^^^^^^
If you are using Django signals in your plugin, we recommend to put them into a ``signals`` submodule. Import it then from the ``AppConfig.ready()`` method.

.. code-block:: python

        def ready(self):
            # Import signals if necessary:
            from . import signals  # NOQA

.. seealso::
    Don't overuse the ``ready`` method. Have a look at the `Django documentation of ready() <https://docs.djangoproject.com/en/2.2/ref/applications/#django.apps.AppConfig.ready>`_.
