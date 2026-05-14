# Talking Mirror

A voice-activated smart mirror that talks back — and not always nicely. Built around a Raspberry Pi Zero 2 W, a two-way acrylic mirror, and a stack of cloud APIs, it wakes up on a keyword, listens to what you say, and replies with a dry sarcastic response through a small speaker. The display shows a minimal animated face that moves when it talks.

The whole thing runs off a single USB power brick and mounts on a wall like a normal mirror. When idle, the screen is off and it just looks like a mirror.

---



---


## Hardware

| Part | Purpose |
|------|---------|
| Raspberry Pi Zero 2 W | Main board — runs everything |
| MicroSD card 32GB | OS and code storage |
| ReSpeaker 2-Mic Pi HAT | Dual microphones, speaker amp, RGB LEDs, and a button — all in one board that stacks directly on the Pi GPIO |
| HP LA2205wg 22" monitor | Display behind the mirror |
| SupremeTech 12×24" two-way acrylic mirror | Reflective from the front, transparent from the back so the screen shows through |
| 8Ω 3W speaker (JST connector) | Plugs straight into the ReSpeaker HAT |
| 5V 3A USB power supply | Powers the Pi via micro-USB |
| 3D printed frame | Holds the mirror and monitor together — STL files in CAD/Frame_stl/ |
| M2.5 standoffs (×4) | Mounts the Pi + HAT stack inside the frame |
| M4 heat-set inserts (×3) + screws | Joins the frame front and back shell |
| Mini-HDMI to HDMI cable | Pi Zero uses mini-HDMI |

The monitor has its own power cable separately. Everything else runs off one USB charger.

---
## Connections
This is insanely simple .

<img width="767" height="507" alt="Schematics" src="https://github.com/user-attachments/assets/9d92d7d4-5462-4abb-85b8-8ec7e4877f1a" />

  
## How it works

The Pi sits behind the monitor inside the 3D printed frame. When you say the wake word ("computer" by default), the ReSpeaker mics pick it up, Porcupine detects it locally, and the mirror wakes up. It records what you say until you stop talking, sends the audio to OpenAI Whisper for transcription, passes the text to GPT-4o-mini with a sarcastic personality prompt, gets a reply, converts it to speech via ElevenLabs, and plays it back through the speaker. The animated face on screen moves while it talks.

The three RGB LEDs on the ReSpeaker HAT act as a status ring — dim blue when idle, green while listening, orange while thinking, purple while talking.

All the heavy AI work (transcription, language model, voice synthesis) happens in the cloud so the Pi Zero doesn't need to do any local inference.

---


## 3D printed frame

The frame is split into three parts so each fits on a standard print bed:


### Front Frame 

<img width="846" height="453" alt="Frame_Front" src="https://github.com/user-attachments/assets/9f3db3a1-2585-4d74-a8be-3984f8b38962" />

### Back Frame

<img width="1104" height="531" alt="Frame_Back" src="https://github.com/user-attachments/assets/28d1f02d-001c-4166-a834-c57a396a6797" />


The mirror sheet sits in the lip with no adhesive — it's held by gravity and the frame. Don't glue it; you'll want to be able to remove it.

## BOM

<img width="1358" height="243" alt="Bom" src="https://github.com/user-attachments/assets/45111de8-bb00-4f32-9292-17fb9a0a6131" />


## Known issues / things to improve

- Pi Zero 2 W gets warm after extended use — the back shell has vent slots but no active cooling
- ElevenLabs free tier runs out fast if you talk to it a lot
- Wake word "computer" has occasional false positives — you can swap it for a custom keyword in config.py using a Porcupine custom model
- The face animation is deliberately minimal; it doesn't lip-sync to phonemes, just opens and closes

---

## License

MIT
