# Changelog #


## 1.0.0 (2016-11-29)

- Now Djmail is compatible only with Django >= 1.8.
- Use celery >= 4.x and remove djcelery dependency.
- Add management command 'djmail_delete_old_messages'.
- Fix Issue #36 'Celery backend fails when CELERY_TASK_SERIALIZER not defined'.
- Minor style improvements and code reorganization.

Note: Special thanks to @mathieuhinderyckx for makeing tjis release posible.


## 0.13.1 (2016-11-14)

- Fix management command 'djmail_retry_send_messages',
  now is compatibile with django 1.10.


## 0.13 (2016-05-29)

- Add compatibility with django 1.10.
  Thanks to @ad-m.


## 0.12 (2015-12-06)

- Pass extra kwargs to EmailMultiAlternatives in MagicMailBuilder.
  Thanks to @ad-m.
- Premailer: Fix call when html is None and create a mixin to be more reusable.
  Thanks to @davidfischer-ch.
- Declare any non-HTML body as text/plain (e.g. JSON).
  Thanks to @davidfischer-ch.
- Fix issue #22: Celery backend: Handle other serializers than pickle (JSON, yaml...)
  Thanks to @davidfischer-ch.


## 0.11 (2015-09-07)

- Translate email subject.
- Now the project will be maintened by David Barragan (@bameda).


## 0.10 (2015-01-21)

- Drop compatibility with django 1.4
- Refactored email rendering making it more efficient using translation switching.
- Better handling different type of emails (html-only, text-only and both).


## 0.9 (2014-09-13)

- code cleaning (pep8) (by @davidfischer-ch)
- fix wrong parameters on management command (by @mathieuhinderyckx)


## 0.8 (2014-07-06)

- Fixed errors' handling in python2.


## 0.7 (2014-06-12)

- Add missing modules not included in the previous version.
- Django 1.4.x support added.
- Minor code cleaning.


## 0.6 (2014-06-05)

- Better control for empty bodies.


## 0.5 (2013-10-27)

- New documentation.
- Runtests improvements.
