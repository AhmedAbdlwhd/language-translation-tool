import pyttsx3


class SpeechService:
    """Text-to-speech service."""

    # Language hints used to match installed voices.
    _VOICE_HINTS = {
        "en": ["english", "en-", "en_", "en-us", "en-gb"],
        "fr": ["french", "fr-", "fr_", "fr-fr", "france"],
        "ar": ["arabic", "ar-", "ar_", "ar-sa", "ar-eg"],
    }

    # Select an installed voice that best matches requested language.
    def _select_voice(self, engine, language_code: str) -> bool:
        voices = engine.getProperty("voices") or []
        hints = self._VOICE_HINTS.get(language_code.lower(), [])

        for voice in voices:
            fields = [str(getattr(voice, "id", "")), str(getattr(voice, "name", ""))]
            for lang in getattr(voice, "languages", []) or []:
                if isinstance(lang, bytes):
                    fields.append(lang.decode("utf-8", errors="ignore"))
                else:
                    fields.append(str(lang))

            lowered = " ".join(fields).lower()
            if any(hint in lowered for hint in hints):
                engine.setProperty("voice", voice.id)
                return True

        return False

    # Speak text using a language-matched voice when available.
    def speak(self, text: str, language_code: str = "en") -> None:
        if not text.strip():
            raise ValueError("No text available for speech.")

        try:
            engine = pyttsx3.init()
        except Exception as error:
            raise ValueError(f"Text-to-speech engine is not available: {error}")

        if not self._select_voice(engine, language_code):
            raise ValueError(
                f"No installed voice found for language '{language_code}'. "
                "Install the corresponding Windows speech voice in Language settings."
            )

        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as error:
            raise ValueError(f"Text-to-speech playback failed: {error}")
        finally:
            try:
                engine.stop()
            except Exception:
                pass