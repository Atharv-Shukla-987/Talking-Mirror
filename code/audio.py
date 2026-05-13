"""
audio.py — Recording via ReSpeaker 2-Mic HAT + playback helpers
"""

import numpy as np
import sounddevice as sd
import subprocess
from scipy.io import wavfile
from config import SAMPLE_RATE, RECORD_DEVICE


def record_until_silence(
    max_duration: float = 10.0,
    silence_threshold: int = 500,
    silence_duration: float = 1.5,
) -> np.ndarray:
    """
    Record from ReSpeaker mics until the user stops talking.

    Returns a mono int16 numpy array.
    """
    chunk_sec      = 0.1
    chunk_samples  = int(SAMPLE_RATE * chunk_sec)
    needed_silent  = int(silence_duration / chunk_sec)
    max_chunks     = int(max_duration / chunk_sec)

    recording    = []
    silent_count = 0

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        device=RECORD_DEVICE,
        dtype="int16",
    ) as stream:
        for _ in range(max_chunks):
            chunk, _ = stream.read(chunk_samples)
            recording.append(chunk.copy())
            rms = int(np.abs(chunk).mean())

            if rms < silence_threshold:
                silent_count += 1
                if (silent_count >= needed_silent
                        and len(recording) > needed_silent):
                    break
            else:
                silent_count = 0

    audio = np.concatenate(recording, axis=0)
    print(f"[audio] recorded {len(audio)/SAMPLE_RATE:.1f}s  "
          f"(peak={int(np.abs(audio).max())})")
    return audio


def save_wav(audio: np.ndarray, path: str = "/tmp/input.wav") -> str:
    """Write a mono int16 array to a WAV file."""
    wavfile.write(path, SAMPLE_RATE, audio)
    return path


def play_audio_file(path: str) -> None:
    """
    Play an audio file (mp3 or wav) through the ReSpeaker speaker output.
    Requires mpg123 for mp3:  sudo apt install mpg123
    """
    if path.endswith(".mp3"):
        subprocess.run(["mpg123", "-q", path], check=False)
    else:
        subprocess.run(["aplay", "-q", path], check=False)


def play_audio_bytes(audio_bytes: bytes, fmt: str = "mp3") -> None:
    """Write raw bytes to /tmp and play them."""
    tmp = f"/tmp/tts_response.{fmt}"
    with open(tmp, "wb") as f:
        f.write(audio_bytes)
    play_audio_file(tmp)
