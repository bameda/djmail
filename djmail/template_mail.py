# -*- coding: utf-8 -*-

from __future__ import print_function

import functools

from django.conf import settings
from django.core import mail
from django.utils import translation
from django.template import loader
from django.template.base import TemplateDoesNotExist


def _get_body_template_prototype():
    return getattr(settings, "DJMAIL_BODY_TEMPLATE_PROTOTYPE",
                   "email/{name}_body.{ext}")


def _get_subject_template_prototype():
    return getattr(settings, "DJMAIL_SUBJECT_TEMPLATE_PROTOTYPE",
                   "email/{name}_subject.txt")


def _get_html_template_extension():
    return getattr(settings, "DJMAIL_HTML_TEMPLATE_EXTENSION",
                   "html")


def _get_txt_template_extension():
    return getattr(settings, "DJMAIL_TXT_TEMPLATE_EXTENSION",
                   "txt")


def _trap_exception(function):
    """
    Simple decorator for catch template
    exceptions. If exception is throwed,
    this decorator by default returns an
    empty string.
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
    Decorator that intercept a language
    attribute and set it on context of
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
        template_ext = _get_html_template_extension()
        template_name = self._body_template_name.format(**{
            "ext": template_ext, "name": self.name})

        return loader.render_to_string(template_name, ctx)

    @_trap_exception
    @_trap_language
    def _render_message_body_as_txt(self, ctx):
        template_ext = _get_txt_template_extension()
        template_name = self._body_template_name.format(**{
            "ext": template_ext, "name": self.name})

        return loader.render_to_string(template_name, ctx)

    def _render_message_subject(self, ctx):
        template_ext = _get_txt_template_extension()
        template_name = self._subject_template_name.format(**{
            "ext": template_ext, "name": self.name})

        subject = loader.render_to_string(template_name, ctx)
        return u" ".join(subject.strip().split())

    def _attach_body_to_email_instance(self, email, ctx):
        body_html = self._render_message_body_as_html(ctx)
        body_txt = self._render_message_body_as_txt(ctx)

        if (isinstance(email, mail.EmailMultiAlternatives)
                and body_txt and body_html):
            email.body = body_txt
            email.attach_alternative(body_html, "text/html")
        else:
            email.body = body_html

    def _attach_subject_to_email_instance(self, email, ctx):
        email.subject = self._render_message_subject(ctx)

    def _make_email_object(self, to, ctx):
        if not isinstance(to, (list, tuple)):
            to = [to]

        email = mail.EmailMultiAlternatives()
        email.to = to

        self._attach_body_to_email_instance(email, ctx)
        self._attach_subject_to_email_instance(email, ctx)
        return email

    def send(self, to, context, **kwargs):
        email = self._make_email_object(to, context)
        return email.send()


class MagicMail(object):
    def __init__(self, email_attr="email", lang_attr="lang"):
        self._email_attr = email_attr
        self._lang_attr = lang_attr

    def __getattr__(self, name):
        def _dynamic_email_generator(to, ctx):
            template_email = TemplateMail()
            return template_email._make_email_object(to, ctx)
