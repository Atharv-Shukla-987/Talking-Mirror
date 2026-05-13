"""
leds.py — APA102 RGB LED control for ReSpeaker 2-Mic HAT
3 onboard LEDs connected via SPI0 (GPIO 10 MOSI, GPIO 11 SCLK)
"""

import spidev
import time
import threading


class APA102:
    def __init__(self, num_leds=3):
        self.num_leds  = num_leds
        self.animating = False
        self.thread    = None

        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 8_000_000

    # ── low-level write ──────────────────────────────────────
    def _write(self, pixels):
        """pixels: list of (r, g, b) tuples, one per LED."""
        start = [0x00] * 4
        end   = [0xFF] * ((self.num_leds // 16) + 1)
        data  = []
        for (r, g, b) in pixels:
            data += [0xE1, int(b), int(g), int(r)]
        self.spi.xfer2(start + data + end)

    def set_all(self, r, g, b):
        self._write([(r, g, b)] * self.num_leds)

    def off(self):
        self.set_all(0, 0, 0)

    # ── animation helpers ───────────────────────────────────
    def stop_animation(self):
        self.animating = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1)

    def _pulse_worker(self, color):
        while self.animating:
            for step in list(range(0, 100, 5)) + list(range(100, 0, -5)):
                if not self.animating:
                    return
                r, g, b = (int(c * step / 100) for c in color)
                self.set_all(r, g, b)
                time.sleep(0.03)

    def pulse(self, color):
        self.stop_animation()
        self.animating = True
        self.thread = threading.Thread(target=self._pulse_worker,
                                       args=(color,), daemon=True)
        self.thread.start()

    def _spinner_worker(self, color):
        idx = 0
        while self.animating:
            pixels = [(0, 0, 0)] * self.num_leds
            pixels[idx % self.num_leds] = color
            self._write(pixels)
            idx += 1
            time.sleep(0.12)

    def spinner(self, color=(80, 40, 0)):
        self.stop_animation()
        self.animating = True
        self.thread = threading.Thread(target=self._spinner_worker,
                                       args=(color,), daemon=True)
        self.thread.start()

    # ── named states ────────────────────────────────────────
    def idle(self):
        self.stop_animation()
        self.set_all(0, 0, 20)          # dim blue

    def listening(self):
        self.pulse((0, 80, 0))          # pulsing green

    def thinking(self):
        self.spinner((80, 40, 0))       # orange spinner

    def speaking(self):
        self.pulse((80, 0, 80))         # pulsing purple

    def error(self):
        self.stop_animation()
        self.set_all(80, 0, 0)          # solid red

    def close(self):
        self.stop_animation()
        self.off()
        self.spi.close()
