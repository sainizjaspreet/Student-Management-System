"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import sys
import asyncio
from django.core.asgi import get_asgi_application
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# On Windows, prefer selector policy to avoid Proactor edge-cases with AnyIO/HTTPX
if sys.platform.startswith('win'):
	try:
		asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
	except Exception:
		pass

application = ASGIStaticFilesHandler(get_asgi_application())
