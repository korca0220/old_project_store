# -*- coding: utf-8 -*-
import os

from django import __version__
from django.core.management import call_command
from django.test import TestCase
from django.test.utils import patch_logger


class ShellPlusCommandTests(TestCase):
    def setUp(self):
        self.project_root = os.path.join('tests', 'testapp')
        self._settings = os.environ.get('DJANGO_SETTINGS_MODULE')
        os.environ['DJANGO_SETTINGS_MODULE'] = 'django_extensions_shell.settings'

    def tearDown(self):
        if self._settings:
            os.environ['DJANGO_SETTINGS_MODULE'] = self._settings

    def test_shell_plus_command(self):
        # XXX: The current shell plus command cannot receive a command and thus seems untestable for now
        # assume correct working since code is based on Django Extensions
        #
        # NOTE: code used from: https://github.com/django/django/blob/master/tests/shell/tests.py
        # with patch_logger('test', 'info') as logger:
        #     call_command(
        #         'shell_plus',
        #         command=(
        #             'import django; from logging import getLogger; '
        #             'getLogger("test").info(django.__version__)'
        #         ),
        #     )
        #     self.assertEqual(len(logger), 1)
        #     self.assertEqual(logger[0], __version__)
        pass
