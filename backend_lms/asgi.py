
import os
from django.core.asgi import get_asgi_application

from django import setup


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_lms.settings')
setup()

application = get_asgi_application()


