import requests
from html import unescape

from config import (
    LIBRETRANSLATE_API_KEY,
    LIBRETRANSLATE_URL,
    MYMEMORY_URL,
)
from languages import LANGUAGE_MAP


class TranslatorService:
    """Service layer for translation operations."""

    @staticmethod
    def _short_error(message: str) -> str:
        compact = " ".join(message.split())
        return compact[:120] + ("..." if len(compact) > 120 else "")

    def translate(self, text: str, source_name: str, target_name: str) -> str:
        """Translate text from source language to target language."""

        if not text.strip():
            raise ValueError("Input text is empty.")

        # Convert language names from UI into provider codes.
        try:
            source_code = LANGUAGE_MAP[source_name]
            target_code = LANGUAGE_MAP[target_name]
        except KeyError as error:
            raise ValueError(f"Unsupported language: {error.args[0]}")

        if source_code == target_code:
            return text

        # Try LibreTranslate first, then fallback to MyMemory.
        libre_error = None
        try:
            return self._translate_with_libre(text, source_code, target_code)
        except ValueError as error:
            libre_error = str(error)

        try:
            return self._translate_with_mymemory(text, source_code, target_code)
        except ValueError as error:
            raise ValueError(
                "Translation failed. Check your internet connection and try again. "
                f"Details: LibreTranslate: {self._short_error(libre_error or '')}; "
                f"MyMemory: {self._short_error(str(error))}"
            )

    def _translate_with_libre(self, text: str, source_code: str, target_code: str) -> str:
        """Translate using LibreTranslate-compatible API."""

        payload = {
            "q": text,
            "source": source_code,
            "target": target_code,
            "format": "text",
        }
        if LIBRETRANSLATE_API_KEY:
            payload["api_key"] = LIBRETRANSLATE_API_KEY

        try:
            response = requests.post(
                LIBRETRANSLATE_URL,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=15,
            )
            response.raise_for_status()
            data = response.json()
            return data["translatedText"]
        except requests.HTTPError as error:
            api_message = ""
            try:
                error_data = response.json()
                api_message = error_data.get("error", "")
            except ValueError:
                api_message = response.text.strip()

            if api_message:
                raise ValueError(f"Translation request failed: {response.status_code} - {api_message}")
            raise ValueError(f"Translation request failed: {error}")
        except requests.RequestException as error:
            raise ValueError(f"Translation request failed: {error}")
        except (KeyError, IndexError, TypeError):
            raise ValueError("Unexpected response format from translation service.")

    def _translate_with_mymemory(self, text: str, source_code: str, target_code: str) -> str:
        """Fallback translation using MyMemory free API."""

        params = {
            "q": text,
            "langpair": f"{source_code}|{target_code}",
        }

        try:
            response = requests.get(MYMEMORY_URL, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            translated_text = data["responseData"]["translatedText"]
            return unescape(translated_text)
        except requests.RequestException as error:
            raise ValueError(f"Translation request failed: {error}")
        except (KeyError, IndexError, TypeError):
            raise ValueError("Unexpected response format from translation service.")