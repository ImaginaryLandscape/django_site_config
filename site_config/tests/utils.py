
settings_overrides = dict(
    INSTALLED_APPS = (
        'django.contrib.admin', 
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions', 
        'django.contrib.messages',
        'django.contrib.staticfiles', 
        'site_config',
        'site_config.backends.model_backend',
    ),
)