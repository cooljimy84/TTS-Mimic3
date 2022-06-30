"""Support for the Mimic3 TTS speech service."""
import logging
import os
import shutil
import subprocess
import tempfile
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from homeassistant.components.tts import CONF_LANG, PLATFORM_SCHEMA, Provider
from homeassistant.const import CONF_TARGET

_LOGGER = logging.getLogger(__name__)

SUPPORT_LANGUAGES = ["en"]

DEFAULT_LANG = "en"

SUPPORT_TARGETS = ["ap", "slt", "slt_hts", "kal", "awb", "kal16", "rms", "awb_time"]

DEFAULT_TARGET = "ap"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_LANG, default=DEFAULT_LANG): vol.In(SUPPORT_LANGUAGES),
        vol.Optional(CONF_TARGET, default=DEFAULT_TARGET): vol.In(SUPPORT_TARGETS)
    }
)


def get_engine(hass, config, discovery_info=None):
    """Set up Mimic3 speech component."""
    if shutil.which("mimic3") is None:
        _LOGGER.error("'mimic3' was not found")
        return False
    return Mimic3Provider(config[CONF_LANG], config[CONF_TARGET])


class Mimic3Provider(Provider):
    """The Mimic3 TTS API provider."""

    def __init__(self, lang, target):
        """Initialize Mimic3 TTS provider."""
        self._lang = lang
        self._target = target
        self.name = "Mimic3"

    @property
    def default_language(self):
        """Return the default language."""
        return self._lang

    @property
    def supported_languages(self):
        """Return list of supported languages."""
        return SUPPORT_LANGUAGES

    @property
    def supported_targets(self):
        """Return list of supported targets."""
        return SUPPORT_TARGETS


    def get_tts_audio(self, message, language, options=None):
        """Load TTS using mimic3."""
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpf:
            fname = tmpf.name

        cmd = ["bash", "-c", "mimic3", "hello there people" ">", fname]
        print(cmd)
        print(fname)
        data = None
        try:
            with open(fname, "rb") as voice:
                data = voice.read()
        except OSError:
            _LOGGER.error("Error trying to read %s", fname)
            return (None, None)
        finally:
            os.remove(ffname)

        if data:
            return ("wav", data)
        return (None, None)
