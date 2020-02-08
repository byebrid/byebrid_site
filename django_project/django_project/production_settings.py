"""
Django settings strictly for the DEVELOPMENT of the website.

WARNING: Make sure the name of THIS file (excluding .py) is the value of the
DJANGO_SETTINGS_MODULE environment variable on the DEPLOYED version of the 
website.
"""
from .base_settings import *

DEBUG = False

# Below settings mainly related to HTTPS as far as I'm aware

# ?: (security.W016) You have 'django.middleware.csrf.CsrfViewMiddleware' in 
# your MIDDLEWARE, but you have not set CSRF_COOKIE_SECURE to True. Using a 
# secure-only CSRF cookie makes it more difficult for network traffic sniffers 
# to steal the CSRF token.
CSRF_COOKIE_SECURE = True

# ?: (security.W008) Your SECURE_SSL_REDIRECT setting is not set to True. 
# Unless your site should be available over both SSL and non-SSL connections, 
# you may want to either set this setting True or configure a load balancer or 
# reverse-proxy server to redirect all connections to HTTPS.
SECURE_SSL_REDIRECT = True

# ?: (security.W012) SESSION_COOKIE_SECURE is not set to True. Using a 
# secure-only session cookie makes it more difficult for network traffic 
# sniffers to hijack user sessions.
SESSION_COOKIE_SECURE = True

# ?: (security.W022) You have not set the SECURE_REFERRER_POLICY setting. 
# Without this, your site will not send a Referrer-Policy header. You should 
# consider enabling this header to protect user privacy.
SECURE_REFERRER_POLICY = 'origin'