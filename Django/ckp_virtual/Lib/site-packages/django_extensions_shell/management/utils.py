# -*- coding: utf-8 -*-
from django_extensions_shell.management.signals import post_command, pre_command


def signalcommand(func):
    """A decorator for management command handle defs that sends out a pre/post signal."""
    def inner(self, *args, **kwargs):
        pre_command.send(self.__class__, args=args, kwargs=kwargs)
        ret = func(self, *args, **kwargs)
        post_command.send(self.__class__, args=args, kwargs=kwargs, outcome=ret)
        return ret
    return inner
