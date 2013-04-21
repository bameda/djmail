.. djmail documentation master file, created by
   sphinx-quickstart on Sat Apr 20 22:16:45 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

djmail
======

Release v\ |version|.

djmail is a :ref:`BSD LIcensed <license>`, simple, powerfull and nonobstructive django email
middleware.


Introduction
------------

djmail consists on this features:

* Can send emails asynchronously and integrates with celery (optional).
* Can retry send failed email messages with crond or celery periodic tasks.
* Can attach priority to email messages.
* Incorporates a simple way to build emails from templates.
* Works transparently. You use a django api as it, without any modifications.


User guide
----------

.. toctree::
   :maxdepth: 2

   quickstart.rst
   usage.rst
   settings.rst
