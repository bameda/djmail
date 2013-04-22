.. djmail documentation master file, created by
   sphinx-quickstart on Sat Apr 20 22:16:45 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

djmail
======

Release v\ |version|.

djmail is a :ref:`BSD LIcensed <license>`, simple, powerful and nonobstructive django email
middleware.


Introduction
------------

djmail involves these features:

* Can send emails asynchronously (it integrates very well with celery)
* Can retry send failed email messages (with crond or celery periodic tasks)
* Can assign deliver priority to a email message.
* Provides a simple way to build email messages from templates.
* Works transparently for your or third party code.


User guide
----------

.. toctree::
   :maxdepth: 2

   quickstart.rst
   usage.rst
   settings.rst
