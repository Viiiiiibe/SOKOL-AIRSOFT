from sokol.settings import *

SECRET_KEY = 'some_secret_key'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


def show_toolbar_callback(*args, **kwargs):
    return False


DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": show_toolbar_callback}
