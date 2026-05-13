"""
ai_brain.py — Whisper STT  +  GPT-4o-mini  +  ElevenLabs TTS
"""

import requests
from openai import OpenAI
from config import (
    OPENAI_API_KEY,
    ELEVENLABS_API_KEY,
    ELEVENLABS_VOICE_ID,
    SARCASTIC_PROMPT,
)

_client = OpenAI(api_key=OPENAI_API_KEY)

# Keep a rolling conversation so the mirror "remembers" context
_history: list[dict] = [{"role": "system", "content": SARCASTIC_PROMPT}]


# ── Speech-to-Text ──────────────────────────────────────────
def transcribe(wav_path: str) -> str:
    """Send WAV file to OpenAI Whisper API and return transcript."""
    with open(wav_path, "rb") as f:
        result = _client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            language="en",
        )
    text = result.text.strip()
    print(f"[STT] '{text}'")
    return text


# ── Language Model ──────────────────────────────────────────
def get_sarcastic_reply(user_text: str) -> str:
    """Send user message to GPT-4o-mini; return sarcastic reply."""
    _history.append({"role": "user", "content": user_text})

    # Keep context window lean (system + last 10 exchanges)
    while len(_history) > 21:
        _history.pop(1)

    response = _client.chat.completions.create(
        model="gpt-4o-mini",
        messages=_history,
        max_tokens=120,
        temperature=0.92,
    )
    reply = response.choices[0].message.content.strip()
    _history.append({"role": "assistant", "content": reply})
    print(f"[GPT] '{reply}'")
    return reply


# ── Text-to-Speech ──────────────────────────────────────────
def text_to_speech(text: str) -> bytes:
    """
    Convert text to MP3 bytes using ElevenLabs Turbo v2.
    Returns raw audio bytes ready to write to a file.
    """
    url = (
        f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
    )
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "model_id": "eleven_turbo_v2",
        "voice_settings": {
            "stability": 0.40,
            "similarity_boost": 0.70,
            "style": 0.50,
            "use_speaker_boost": True,
        },
    }
    r = requests.post(url, json=payload, headers=headers, timeout=15)
    r.raise_for_status()
    return r.content


def reset_conversation() -> None:
    """Clear conversation history (keep system prompt)."""
    _history.clear()
    _history.append({"role": "system", "content": SARCASTIC_PROMPT})
