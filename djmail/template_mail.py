# -*- coding: utf-8 -*-

from __future__ import print_function

import functools
import traceback
import sys

from django.conf import settings
from django.core import mail
from django.utils import translation
from django.template import loader, TemplateDoesNotExist

from . import models

# Python 3 compatibility
if sys.version_info[0] == 3:
    string_types = (str,)
else:
    string_types = (str, unicode,)


def _get_body_template_prototype():
    return getattr(settings, "DJMAIL_BODY_TEMPLATE_PROTOTYPE",
                   "emails/{name}-body-{type}.{ext}")


def _get_subject_template_prototype():
    return getattr(settings, "DJMAIL_SUBJECT_TEMPLATE_PROTOTYPE",
                   "emails/{name}-subject.{ext}")


def _get_template_extension():
    return getattr(settings, "DJMAIL_TEMPLATE_EXTENSION", "html")


def _trap_exception(function):
    """
    Simple decorator for catch template exceptions. If exception is throwed,
    this decorator by default returns an empty string.
    """
    @functools.wraps(function)
    def _decorator(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except TemplateDoesNotExist as e:
            return u""

    return _decorator


def _trap_language(function):
    """
    Decorator that intercept a language attribute and set it on context of
    the execution.
    """
    @functools.wraps(function)
    def _decorator(self, ctx):
        language_new = None
        language_old = translation.get_language()

        # If attr found on context, set a new language
        if "lang" in ctx:
            language_new = ctx["lang"]
            translation.activate(language_new)

        try:
            return function(self, ctx)
        finally:
            if language_new is not None:
                translation.activate(language_old)

    return _decorator


class TemplateMail(object):
    name = None

    def __init__(self, name=None):
        self._email = None

        if name is not None:
            self.name = name

        self._initialize_settings()

    def _initialize_settings(self):
        self._body_template_name = _get_body_template_prototype()
        self._subject_template_name = _get_subject_template_prototype()

    @_trap_exception
    @_trap_language
    def _render_message_body_as_html(self, ctx):
        template_ext = _get_template_extension()
        template_name = self._body_template_name.format(**{
            "ext": template_ext, "name": self.name, "type":"html"})

        return loader.render_to_string(template_name, ctx)

    @_trap_exception
    @_trap_language
    def _render_message_body_as_txt(self, ctx):
        template_ext = _get_template_extension()
        template_name = self._body_template_name.format(**{
            "ext": template_ext, "name": self.name, "type": "text"})

        return loader.render_to_string(template_name, ctx)

    def _render_message_subject(self, ctx):
        template_ext = _get_template_extension()
        template_name = self._subject_template_name.format(**{
            "ext": template_ext, "name": self.name})

        subject = loader.render_to_string(template_name, ctx)
        return u" ".join(subject.strip().split())

    def _attach_body_to_email_instance(self, email, ctx):
        body_html = self._render_message_body_as_html(ctx)
        body_txt = self._render_message_body_as_txt(ctx)

        if isinstance(email, mail.EmailMultiAlternatives):
            email.body = body_txt
            email.attach_alternative(body_html, "text/html")
        else:
            email.body = body_txt

    def _attach_subject_to_email_instance(self, email, ctx):
        email.subject = self._render_message_subject(ctx)

    def make_email_object(self, to, ctx, **kwargs):
        if not isinstance(to, (list, tuple)):
            to = [to]

        email = mail.EmailMultiAlternatives(**kwargs)
        email.to = to

        self._attach_body_to_email_instance(email, ctx)
        self._attach_subject_to_email_instance(email, ctx)
        return email

    def send(self, to, context, **kwargs):
        email = self.make_email_object(to, context, **kwargs)
        return email.send()


class MagicMailBuilder(object):
    def __init__(self, email_attr="email", lang_attr="lang",
                 template_mail_cls=TemplateMail):
        self._email_attr = email_attr
        self._lang_attr = lang_attr
        self._template_mail_cls = template_mail_cls

    def __getattr__(self, name):
        def _dynamic_email_generator(to, ctx, priority=models.PRIORITY_STANDARD):
            lang = None
            to = None

            if not isinstance(to, string_types):
                if not hasattr(to, self._email_attr):
                    raise AttributeError(
                        "to object does not "
                        "have {0} attribute".format(self._email_attr))

                lang = getattr(to, self._lang_attr, None)
                to = getattr(to, self._email_attr)

            if lang is not None:
                ctx["lang"] = lang

            template_email = self._template_mail_cls(name=name)
            email_instance = template_email.make_email_object(to, ctx)
            email_instance.priority = priority

            return email_instance

        return _dynamic_email_generator
