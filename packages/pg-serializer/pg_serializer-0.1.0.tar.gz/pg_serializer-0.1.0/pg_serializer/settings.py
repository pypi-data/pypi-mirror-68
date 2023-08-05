from django.conf import settings
from django.test.signals import setting_changed

from rest_framework import settings

DJANGO_SETTINGS_KEY = "PG_SERIALIZER"

DEFAULTS = {
    "COERCE_DECIMAL_TO_STRING": True,
    "JSON_AS_BYTES": False,
}


# List of settings that may be in string import notation.
IMPORT_STRINGS = ()


# List of settings that have been removed
REMOVED_SETTINGS = ()


class APISettings(settings.APISettings):
    @property
    def user_settings(self):
        if not hasattr(self, "_user_settings"):
            self._user_settings = getattr(settings, DJANGO_SETTINGS_KEY, {})
        return self._user_settings

    def __check_user_settings(self, user_settings):
        for setting in REMOVED_SETTINGS:
            if setting in user_settings:
                raise RuntimeError(
                    f"The '{setting}' setting has been removed. "
                    "Please refer to the documentation for available settings."
                )
        return user_settings


api_settings = APISettings(None, DEFAULTS, IMPORT_STRINGS)


def reload_api_settings(*args, **kwargs):
    setting = kwargs["setting"]
    if setting == DJANGO_SETTINGS_KEY:
        api_settings.reload()


setting_changed.connect(reload_api_settings)
