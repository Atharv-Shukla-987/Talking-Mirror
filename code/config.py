# ─── API Keys ───────────────────────────────────────────────
# Get free keys from:
# Picovoice  → https://picovoice.ai/
# OpenAI     → https://platform.openai.com/
# ElevenLabs → https://elevenlabs.io/

PICOVOICE_ACCESS_KEY = "YOUR_PICOVOICE_KEY"
OPENAI_API_KEY       = "YOUR_OPENAI_KEY"
ELEVENLABS_API_KEY   = "YOUR_ELEVENLABS_KEY"
ELEVENLABS_VOICE_ID  = "21m00Tcm4TlvDq8ikWAM"   # Rachel (snarky default)

# ─── Wake / Sleep ────────────────────────────────────────────
WAKE_WORD   = "computer"    # Built-in Porcupine keyword (free)
SLEEP_WORDS = ["goodbye", "shut up", "go to sleep", "stop"]

# ─── Audio ───────────────────────────────────────────────────
SAMPLE_RATE    = 16000
RECORD_DEVICE  = 1          # ReSpeaker (verify with: arecord -l)
PLAYBACK_DEVICE = 1

# ─── Hardware ────────────────────────────────────────────────
BUTTON_GPIO = 17            # ReSpeaker onboard button
LED_COUNT   = 3             # ReSpeaker has 3 APA102 LEDs

# ─── Personality ─────────────────────────────────────────────
SARCASTIC_PROMPT = """You are a magic mirror with a dry, sarcastic, witty personality —
like a mix of Chandler Bing and a tired British butler who has seen too much.
You roast the user gently but lovingly. Keep replies under 2 sentences.
Be clever, ironic, and occasionally dramatic — never mean or offensive.
You live in a mirror and are mildly offended to be woken up every time."""
