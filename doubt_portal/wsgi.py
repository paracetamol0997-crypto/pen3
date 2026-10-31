"""
WSGI config for doubt_portal project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

# Ensure vendor folder is available if deployed without pip
BASE_DIR = Path(__file__).resolve().parent.parent
vendor_dir = BASE_DIR / 'vendor'
if vendor_dir.exists() and str(vendor_dir) not in sys.path:
    sys.path.insert(0, str(vendor_dir))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'doubt_portal.settings')

application = get_wsgi_application()

# Vercel entrypoint variable
app = application
