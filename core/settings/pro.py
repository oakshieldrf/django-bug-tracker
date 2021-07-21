from .base import *

DEBUG = False

ADMINS = (
    ('admin', 'admin@mail.com'),
)

ALLOWED_HOSTS = ['bug-tracker.sophiaeternum.com', 'www.bug-tracker.sophiaeternum.com']

SECURE_CONTENT_TYPE_NOSNIFF  = True 
SECURE_BROWSER_XSS_FILTER = True 
SECURE_SSL_REDIRECT  = False 
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_SECURE = True
