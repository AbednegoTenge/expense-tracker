"""
WSGI config for expensetracker project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys

path = "/home/abednego-tenge/Desktop/Projects/expensetracker"
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "expensetracker.settings"
)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expensetracker.settings')

application = get_wsgi_application()
