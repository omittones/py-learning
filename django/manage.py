#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import myproject.settings

# ENABLE_DEBUG = False


def main():

    # if ENABLE_DEBUG:
    #     try:
    #         import ptvsd
    #         ptvsd.enable_attach(address = ('localhost', 8080))
    #         print("Started remote debugger")
    #     except:
    #         pass

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    if sys.argv[1] == 'test':
        myproject.settings.TESTING = True
    elif sys.argv[1].startswith('run'):
        sys.argv[1] = 'runserver'

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
