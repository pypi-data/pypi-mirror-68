GDAPS Frontend Support
======================

GDAPS supports frontends for building e.g. SPA applications.
ATM only Vue.js ist supported well, but PRs are welcome to add more (Angular,
React?). Even PySide or Qt5 would be possible.


Install
-------

.. code-block:: bash

    pip install gdaps-frontend

Add ``gdaps.frontend`` to ``INSTALLED_APPS``, **before** ``gdaps``.

The included `gdaps.frontend` package provides basic tools which then can be extended by other plugins, like `gdaps-frontend-vue`. You have to install at least one frontend plugin, e.g.

.. code-block:: bash

    pip install gdaps-frontend-vue


GDAPS detects it automatically and makes the "vue" FRONTEND_ENGINE available.

.. code-block:: python

    # settings.py

    GDAPS = {
        "FRONTEND_ENGINE": "vue",
        "FRONTEND_DIR": "frontend",
        "FRONTEND_PKG_MANAGER": "",
    }

There are some keys here to configure:

FRONTEND_ENGINE (mandatory)
    The engine which is used for setting up a frontend.
    ATM it can only be "vue" or "pyside".
    See the [gdaps-frontend-vue package](gdaps-frontend-vue.readthedocs.org)

FRONTEND_DIR (optional)
    This is the directory for the frontend, relative to DJANGO_ROOT.
    **Default is "frontend".**

FRONTEND_PKG_MANAGER (optional)
    This is the package manager used to init/install packages.
    ATM you can use "yarn" or "npm". **Default is *npm*.**


Management Commands
-------------------

There is a new
management command available. Set the ``GDAPS["FRONTEND_ENGINE"]`` to your desired engine ("vue", "pyside"), and call:

.. code-block:: bash

    ./manage.py initfrontend

This creates a /frontend/ directory in the project root, and installs a frontend application there. The type of frontend (and installation) depends on what you have selected in ``GDAPS["FRONTEND_ENGINE"]``.

So all you have to do is:

#. Add ``gdaps.frontend`` to ``INSTALLED_APPS`` (before ``gdaps``)
#. Install a frontend plugin, like `pip install gdaps-frontend-vue`.
#. Execute ``./manage.py initfrontend``
#. Call ``./manage.py startplugin fooplugin``
#. Call ``./manage.py syncplugins``
#. start ``yarn serve`` in the *frontend* directory
#. start Django server using ``./manage.py runserver``

To remove a plugin from the frontend, just remove the backend part (remove it from INSTALLED_APPS or uninstall it using pip) and call ``manage.py syncplugins`` again. It will take care of the database models, and the uninstallation of the frontend part.


License
=======

I'd like to give back what I received from many Open Source software packages, and keep this
library as open as possible, and it should stay this way.
GDAPS is licensed under the `General Public License, version 3 <https://www.gnu.org/licenses/gpl-3.0-standalone.html>`_.
