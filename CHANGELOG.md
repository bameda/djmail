# Changelog #


## 0.12 (unreleased)

- Pass extra kwargs to EmailMultiAlternatives in MagicMailBuilder.
- Premailer: Fix call when html is None and create a mixin to be more reusable.
- Declare any non-HTML body as text/plain (e.g. JSON).


## 0.11 (2014-09-07)

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
