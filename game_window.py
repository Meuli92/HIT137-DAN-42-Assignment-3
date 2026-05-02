import tkinter as tk
from image_processor import ImageProcessor
from game_state import GameState

class GameWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.processor = None
        self.state = None
    
    def setup_layout(self):
        """Build the side-by-side layout, buttons, and stat labels."""
        pass
    
    def load_image(self):
        """Open file dialog, trigger processor and state, refresh display."""
        pass
    
    def display_images(self, original, modified):
        """Render both images side by side on canvas."""
        pass
    
    def draw_circle(self, image, region: dict, colour: str):
        """Draw circle on both images. colour is 'red' (found) or 'blue' (revealed)."""
        pass
    
    def handle_click(self, event):
        """Handle click on modified image, delegate to game_state."""
        pass
    
    def reveal_all(self):
        """Mark all unfound differences with blue circles."""
        pass
    
    def update_stats(self):
        """Refresh remaining count and mistakes display."""
        pass