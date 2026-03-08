import os

# Primary translation provider URL.
LIBRETRANSLATE_URL = os.getenv("LIBRETRANSLATE_URL", "https://translate.argosopentech.com/translate")
# Optional key for LibreTranslate instances that require auth.
LIBRETRANSLATE_API_KEY = os.getenv("LIBRETRANSLATE_API_KEY", "")
# Fallback provider URL.
MYMEMORY_URL = os.getenv("MYMEMORY_URL", "https://api.mymemory.translated.net/get")