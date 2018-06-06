djmail
======

.. image:: https://travis-ci.org/bameda/djmail.svg?branch=master
    :target: https://travis-ci.org/bameda/djmail


djmail is a BSD Licensed, simple and nonobstructive django email middleware.

Why use djmail? Because it:

- Sends emails asynchronously without additional libraries.
- Sends emails using celery tasks.
- Can retry sending failed messages (with cron task or celery periodic task).
- Can assign delivery priority.
- Has a powerfull class to build emails from templates.
- Works transparently (works as middleware for native django email backends)

djmail was created by Andrey Antukh (@niwinz) and is maintened by David Barragán (@bameda).

You can read the full documentation at https://bameda.github.io/djmail/.
