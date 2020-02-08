"""
Django settings strictly for the DEVELOPMENT of the website.

WARNING: These settings should only be used whilst developing the website! The
production/deployed website should use production_settings.py.
"""
from .base_settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True