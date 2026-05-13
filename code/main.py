"""
main.py — Sarcastic Mirror  |  Pi Zero 2 W + ReSpeaker 2-Mic HAT
─────────────────────────────────────────────────────────────────
Flow:
  idle  →  wake word / button  →  listen  →  STT  →  GPT  →  TTS  →  idle
"""

import time

import numpy as np
import pvporcupine
import RPi.GPIO as GPIO
import sounddevice as sd

from ai_brain import get_sarcastic_reply, reset_conversation, text_to_speech, transcribe
from audio import play_audio_bytes, record_until_silence, save_wav
from config import (
    BUTTON_GPIO,
    LED_COUNT,
    PICOVOICE_ACCESS_KEY,
    RECORD_DEVICE,
    SLEEP_WORDS,
    WAKE_WORD,
)
from face import MirrorFace
from leds import APA102


# ── hardware init ────────────────────────────────────────────
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

leds = APA102(num_leds=LED_COUNT)
face = MirrorFace(fullscreen=True)

porcupine = pvporcupine.create(
    access_key=PICOVOICE_ACCESS_KEY,
    keywords=[WAKE_WORD],
)


# ── helpers ──────────────────────────────────────────────────
def speak(text: str) -> None:
    """Say something out loud while animating the face."""
    print(f"[Mirror] {text}")
    leds.speaking()
    face.start_talking()
    try:
        audio_bytes = text_to_speech(text)
        play_audio_bytes(audio_bytes)
    except Exception as exc:
        print(f"[TTS error] {exc}")
    face.stop_talking()


def wait_for_wake() -> None:
    """Block until wake word heard or button pressed."""
    leds.idle()
    face.hide()
    print(f"\n[Mirror] Sleeping… say '{WAKE_WORD}' or press button.")

    with sd.RawInputStream(
        samplerate=porcupine.sample_rate,
        blocksize=porcupine.frame_length,
        dtype="int16",
        channels=1,
        device=RECORD_DEVICE,
    ) as stream:
        while True:
            pcm = np.frombuffer(
                stream.read(porcupine.frame_length)[0], dtype=np.int16
            )
            if porcupine.process(pcm) >= 0:
                print("[Mirror] Wake word detected!")
                return
            if GPIO.input(BUTTON_GPIO) == GPIO.LOW:
                print("[Mirror] Button pressed!")
                time.sleep(0.3)    # debounce
                return


# ── conversation session ─────────────────────────────────────
def run_conversation() -> None:
    face.show()
    reset_conversation()
    speak("Oh look, you're back. What pearls of wisdom shall I endure today?")

    consecutive_blanks = 0

    while True:
        leds.listening()
        audio = record_until_silence()
        save_wav(audio)

        leds.thinking()
        try:
            user_text = transcribe("/tmp/input.wav")
        except Exception as exc:
            print(f"[STT error] {exc}")
            speak("I couldn't catch that. Try speaking at a volume above 'mumble'.")
            continue

        if not user_text.strip():
            consecutive_blanks += 1
            if consecutive_blanks >= 2:
                speak("Clearly you've nothing to say. I'll go back to ignoring you.")
                return
            continue
        consecutive_blanks = 0

        # Sleep / dismiss commands
        if any(w in user_text.lower() for w in SLEEP_WORDS):
            speak("Finally. Some peace and quiet. Goodbye.")
            return

        try:
            reply = get_sarcastic_reply(user_text)
            speak(reply)
        except Exception as exc:
            print(f"[GPT error] {exc}")
            leds.error()
            speak("Something broke. Even I'm embarrassed.")
            time.sleep(2)


# ── main loop ────────────────────────────────────────────────
def main() -> None:
    print("=== Sarcastic Mirror Starting ===")
    try:
        while True:
            wait_for_wake()
            run_conversation()
    except KeyboardInterrupt:
        print("\n[Mirror] Shutting down gracefully…")
    finally:
        leds.close()
        face.quit()
        GPIO.cleanup()
        porcupine.delete()
        print("[Mirror] Goodbye.")


if __name__ == "__main__":
    main()
