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

djmail consists on theese main notable features:

* Can send emails asyncronously and integrates with celery (optional).
* Can retry send failure messages with system cron or celery periodic tasks.
* Can assign send priority on a email object.
* Incorporates a simple way to build emails from templates.
* Works transparently. You use a django api as it without modifications.


User guide
----------

.. toctree::
   :maxdepth: 2

   quickstart.rst
   usage.rst
   settings.rst
