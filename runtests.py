# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
sys.path.insert(0, 'testing')


if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    args = sys.argv
    args.insert(1, "test")

    execute_from_command_line(args)
