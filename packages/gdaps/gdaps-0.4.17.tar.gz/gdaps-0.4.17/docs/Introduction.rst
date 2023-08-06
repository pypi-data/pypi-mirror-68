Introduction
============

This library allows Django to make real "pluggable" apps.

A standard Django "app" is *reusable* (if done correctly), but is not *pluggable*,
like being distributed and "plugged" into a Django main application without modifications. GDAPS is filling this gap.

The reason you want to use GDAPS is: **you want to create an application that should be extended via plugins**. GDAPS consists of a few bells and twistles where Django lacks "automagic":

GDAPS apps...
* are automatically found using setuptools' entry points
* can provide their own URLs which are included and merged into urlpatterns automatically
* can define ``Interfaces``, that other GDAPS apps then can implement
* can provide Javascript frontends that are found and compiled automatically (WorkInProgress)


GDAPS working modes
-------------------

The "observer pattern" plugin system is completely decoupled from the PluginManager
(which manages GDAPS pluggable Django apps), so basically you have two choices to use GDAPS:

Simple
    Use :ref:`Interfaces`, and :ref:`Implementations`  **without a plugin/module system**. It's not necessary to divide your application into GDAPS apps to use GDAPS.
    Just code your application as a monolithic django application have an
    easy-to-use "observer pattern" plugin system.

    * import gdaps
    * Define an interface
    * Create one or more implementations for it and
    * iterate over the interface to get all the implementations.

    Just *importing* the python files with your implementations will make them work automatically.

    Use this if you just want to structure your Django software using an "observer pattern".
    This is used  within  GDAPS itself.

Full
    Use GDAPS as a **full-featured system to create modular applications**.

    * Add "gdaps" to your INSTALLED_APPS.
    * Create plugins using the ``startplugin`` managemant command, and install them via pip, (or add them to your INSTALLED_APPS too).

    You have a :class:`gdaps.PluginManager` available then, and after a ``manage.py migrate``
    and ``manage.py syncplugins``,
    Django will have all GDAPS plugins recognized as models too, so you can easily
    administer them in your Django admin.

    This "full" usage enables you to create fully-fledged extensible applications enabling
    third party plugins that can be distributed via PyPi.

    See :doc:`usage` for further instructions.
