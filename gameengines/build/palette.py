import numpy as np


class Palette:

    def __init__(self):
        self.data = None

    def load(self, file_path: str):

        with open(file_path, 'rb') as f:
            data = f.read(768)  # first 768 bytes = 256 colors × 3 components

        # Interpret as 256 × 3 uint8 array
        palette = np.frombuffer(data, dtype=np.uint8).reshape((256, 3))

        # Build palettes are 6-bit values (0–63), scale to 0–255
        palette = (palette * 4).clip(0, 255).astype(np.uint8)

        self.data = palette
