"""
face.py — Pygame animated sarcastic face for the mirror display.

Runs in its own daemon thread so main.py can control it via simple calls.
Black background = invisible behind the two-way mirror acrylic when idle.
White/light-blue elements glow through the mirror when visible.
"""

import math
import threading
import time

import pygame


class MirrorFace:
    def __init__(self, fullscreen: bool = True):
        pygame.init()
        if fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((800, 480))
        pygame.display.set_caption("Sarcastic Mirror")
        pygame.mouse.set_visible(False)

        self.W, self.H = self.screen.get_size()
        self.clock     = pygame.time.Clock()

        self._visible  = False
        self._talking  = False
        self._blink    = False
        self._running  = True
        self._mouth_t  = 0.0           # time offset for mouth animation

        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    # ── public controls ─────────────────────────────────────
    def show(self):
        self._visible = True

    def hide(self):
        self._visible = False
        self._talking = False

    def start_talking(self):
        self._visible = True
        self._talking = True
        self._mouth_t = time.time()

    def stop_talking(self):
        self._talking = False

    def quit(self):
        self._running = False
        pygame.quit()

    # ── render loop ─────────────────────────────────────────
    def _loop(self):
        FACE_COLOR = (200, 220, 255)    # cool white-blue glow
        BG         = (0, 0, 0)

        while self._running:
            # pump events so window stays responsive
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

            self.screen.fill(BG)

            if self._visible:
                cx = self.W // 2
                cy = self.H // 2 - 20

                # ── eyebrows (slightly raised = perpetually judgy) ──
                for side in (-1, 1):
                    ex = cx + side * 150
                    pygame.draw.line(
                        self.screen, FACE_COLOR,
                        (ex - 55, cy - 115), (ex + 55, cy - 105), 5
                    )

                # ── eyes ──────────────────────────────────────────
                eye_w, eye_h = 70, 34
                for side in (-1, 1):
                    ex = cx + side * 150
                    # eyelid (covers top half when blinking)
                    blink_h = eye_h if not self._blink else eye_h // 2
                    pygame.draw.ellipse(
                        self.screen, FACE_COLOR,
                        (ex - eye_w // 2, cy - 80, eye_w, blink_h), 0
                    )
                    # pupil
                    pygame.draw.circle(
                        self.screen, (30, 30, 60),
                        (ex + 5 * side, cy - 65), 10
                    )

                # ── mouth ─────────────────────────────────────────
                if self._talking:
                    phase = time.time() - self._mouth_t
                    # oscillate between slightly open and wide open
                    open_frac = 0.25 + 0.75 * abs(math.sin(phase * 10))
                else:
                    open_frac = 0.10   # thin resting smirk

                mouth_h = max(4, int(50 * open_frac))
                mouth_w = 160
                pygame.draw.ellipse(
                    self.screen, FACE_COLOR,
                    (cx - mouth_w // 2, cy + 50, mouth_w, mouth_h), 3
                )

            pygame.display.flip()
            self.clock.tick(30)

    # ── blink helper (call from outside if desired) ─────────
    def blink_once(self):
        self._blink = True
        time.sleep(0.12)
        self._blink = False
