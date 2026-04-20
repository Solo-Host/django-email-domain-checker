SECRET_KEY = "test-secret-key-not-for-production"

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "email_domain_checker",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

USE_TZ = True
