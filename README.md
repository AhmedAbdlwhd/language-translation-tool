# Language Translation Tool (PyQt6)

A local desktop language translation application built with Python and PyQt6.

## Features

- Input text box for source text
- Source language selector
- Target language selector
- Translate button with API fallback strategy
- Output text box for translated text
- Copy translated text to clipboard
- Text-to-speech (Speak) for translated text
- Error handling with clear user messages
- Basic usability enhancements (busy state + status updates)

## Tech Stack

- Python 3.10+
- PyQt6 (desktop GUI)
- Requests (HTTP API calls)
- pyttsx3 (offline text-to-speech engine)

## Project Structure

- `main.py` — app entry point
- `ui.py` — PyQt6 window, widgets, event handlers
- `translator.py` — translation service layer with provider fallback
- `speech.py` — text-to-speech service layer
- `languages.py` — language display-name to code mapping
- `config.py` — environment-based provider configuration

## Installation

1. Create and activate virtual environment.
2. Install dependencies:

```powershell
pip install -r requirements.txt
```

## Running the App

Run from project root:

```powershell
python .\main.py
```

## Environment Variables

Optional provider settings (defaults are already configured in `config.py`):

- `LIBRETRANSLATE_URL`
- `LIBRETRANSLATE_API_KEY`
- `MYMEMORY_URL`

Example (PowerShell, current session):

```powershell
$env:LIBRETRANSLATE_URL = "https://translate.argosopentech.com/translate"
$env:LIBRETRANSLATE_API_KEY = ""
$env:MYMEMORY_URL = "https://api.mymemory.translated.net/get"
```

## Troubleshooting

- **Translation fails**
  - Check internet connection.
  - Try again (free providers can be rate-limited or temporarily unavailable).
  - Verify environment variable values if customized.

- **Speak works only for English**
  - Install corresponding Windows Speech voices for Arabic/French in:
    Settings → Time & Language → Language & Region → Language options → Speech.

- **No output copied**
  - Ensure translation succeeded and output text is visible before clicking Copy.

## Known Limitations

- Free public translation endpoints may have rate limits or intermittent downtime.
- Voice quality/availability depends on installed system TTS voices.

## Future Improvements

- Add asynchronous translation worker thread to keep UI fully responsive on slow networks.
- Add unit tests for translator and speech services.
- Add optional provider selector in settings.
- Package as standalone executable for easier distribution.
