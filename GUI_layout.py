import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
 
from image_processor import ImageProcessor
from game_state import GameState
 

class SpotDifferenceGUI:
    CANVAS_WIDTH = 500
    CANVAS_HEIGHT = 400

    def __init__(self, root):
        self.root = root
        self.root.title("Spot the Difference Game")
        self.root.geometry("1100x700")
        self.root.resizable(False, False)

        self.processor = ImageProcessor()
        self.state = GameState()
        self.original_photo = None
        self.modified_photo = None
        self.original_display = None
        self.modified_display = None
        self._drawn_regions = []
 
        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root,
            text="Spot the Difference Game",
            font=("Arial", 22, "bold")
        )
        title_label.pack(pady=10)

        # Top button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        self.load_button = tk.Button(
            button_frame,
            text="Load Image",
            font=("Arial", 12),
            width=15,
            command=self.load_image
        )
        self.load_button.grid(row=0, column=0, padx=10)

        self.reveal_button = tk.Button(
            button_frame,
            text="Reveal Differences",
            font=("Arial", 12),
            width=18,
            command=self.reveal_differences
        )
        self.reveal_button.grid(row=0, column=1, padx=10)

        self.restart_button = tk.Button(
            button_frame,
            text="Restart",
            font=("Arial", 12),
            width=15,
            command=self.restart_game
        )
        self.restart_button.grid(row=0, column=2, padx=10)

        # Score information frame
        info_frame = tk.Frame(self.root)
        info_frame.pack(pady=10)

        self.remaining_label = tk.Label(
            info_frame,
            text="Remaining Differences: 5",
            font=("Arial", 14)
        )
        self.remaining_label.grid(row=0, column=0, padx=30)

        self.mistakes_label = tk.Label(
            info_frame,
            text="Mistakes: 0 / 3",
            font=("Arial", 14)
        )
        self.mistakes_label.grid(row=0, column=1, padx=30)

        self.status_label = tk.Label(
            info_frame,
            text="Please load an image to start.",
            font=("Arial", 14)
        )
        self.status_label.grid(row=0, column=2, padx=30)

        # Image display frame
        image_frame = tk.Frame(self.root)
        image_frame.pack(pady=20)

        # Original image section
        original_frame = tk.Frame(image_frame)
        original_frame.grid(row=0, column=0, padx=20)

        original_title = tk.Label(
            original_frame,
            text="Original Image",
            font=("Arial", 14, "bold")
        )
        original_title.pack(pady=5)

        self.original_canvas = tk.Canvas(
            original_frame,
            width=500,
            height=400,
            bg="lightgray",
            relief=tk.SUNKEN,
            borderwidth=2
        )
        self.original_canvas.pack()

        # Modified image section
        modified_frame = tk.Frame(image_frame)
        modified_frame.grid(row=0, column=1, padx=20)

        modified_title = tk.Label(
            modified_frame,
            text="Modified Image - Click Here",
            font=("Arial", 14, "bold")
        )
        modified_title.pack(pady=5)

        self.modified_canvas = tk.Canvas(
            modified_frame,
            width=500,
            height=400,
            bg="lightgray",
            relief=tk.SUNKEN,
            borderwidth=2
        )
        self.modified_canvas.pack()

        self.modified_canvas.bind("<Button-1>", self.check_click)

    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[
                ("Image Files", "*.jpg *.jpeg *.png *.bmp"),
                ("JPEG Files", "*.jpg *.jpeg"),
                ("PNG Files", "*.png"),
                ("BMP Files", "*.bmp")
            ]
        )

        if file_path:
            success = self.processor.load_image(file_path)
            if not success:
                messagebox.showerror("Error", "Could not load image. Please try another file.")
                return
            self.state.new_round(self.processor.get_regions())
            self.original_display = self.processor.get_original()
            self.modified_display = self.processor.get_modified()
            orig = cv2.cvtColor(cv2.resize(self.original_display, (self.CANVAS_WIDTH, self.CANVAS_HEIGHT)), cv2.COLOR_BGR2RGB)
            mod  = cv2.cvtColor(cv2.resize(self.modified_display,  (self.CANVAS_WIDTH, self.CANVAS_HEIGHT)), cv2.COLOR_BGR2RGB)
            self.original_photo = ImageTk.PhotoImage(Image.fromarray(orig))
            self.modified_photo = ImageTk.PhotoImage(Image.fromarray(mod))
            self.original_canvas.create_image(0, 0, anchor=tk.NW, image=self.original_photo)
            self.modified_canvas.create_image(0, 0, anchor=tk.NW, image=self.modified_photo)
            self.remaining_label.config(text=f"Remaining Differences: {self.state.get_remaining()}")
            self.mistakes_label.config(text=f"Mistakes: {self.state.get_mistakes()} / 3")
            self.status_label.config(text="Image loaded. Find the 5 differences!")
  
    def reveal_differences(self):
        if not self.processor.is_loaded():
            return
        for region in self.state.get_unfound_regions():
            cv2.circle(self.original_display, (region['x'], region['y']), region['r'], (255, 0, 0), 3)
            cv2.circle(self.modified_display,  (region['x'], region['y']), region['r'], (255, 0, 0), 3)
        orig = cv2.cvtColor(cv2.resize(self.original_display, (self.CANVAS_WIDTH, self.CANVAS_HEIGHT)), cv2.COLOR_BGR2RGB)
        mod  = cv2.cvtColor(cv2.resize(self.modified_display,  (self.CANVAS_WIDTH, self.CANVAS_HEIGHT)), cv2.COLOR_BGR2RGB)
        self.original_photo = ImageTk.PhotoImage(Image.fromarray(orig))
        self.modified_photo = ImageTk.PhotoImage(Image.fromarray(mod))
        self.original_canvas.create_image(0, 0, anchor=tk.NW, image=self.original_photo)
        self.modified_canvas.create_image(0, 0, anchor=tk.NW, image=self.modified_photo)
        self.status_label.config(text="Differences revealed. Load a new image to play again.")
        self.modified_canvas.unbind("<Button-1>")

    def restart_game(self):
        self.remaining_label.config(text="Remaining Differences: 5")
        self.mistakes_label.config(text="Mistakes: 0 / 3")
        self.status_label.config(text="Game restarted.")
        self.original_canvas.delete("all")
        self.modified_canvas.delete("all")
        self.modified_canvas.bind("<Button-1>", self.check_click)

        self.processor = ImageProcessor()
        self.state = GameState()
        self.original_display = None
        self.modified_display = None
        self._drawn_regions = []

    def check_click(self, event):
        if not self.processor.is_loaded():
            return

        scale_x = self.original_display.shape[1] / self.CANVAS_WIDTH
        scale_y = self.original_display.shape[0] / self.CANVAS_HEIGHT

        result = self.state.check_click(
            int(event.x * scale_x),
            int(event.y * scale_y)
        )

   
        if result == 'hit':

            self.remaining_label.config(
                text=f"Remaining Differences: {self.state.get_remaining()}"
            )
            self.mistakes_label.config(
                text=f"Mistakes: {self.state.get_mistakes()} / 3"
            )

            self.status_label.config(
                text="Correct! Keep going.",
                fg="green"
            )

            if self.state.is_complete():
                messagebox.showinfo(
                    "Well done!",
                    "You found all 5 differences!\nLoad a new image to play again."
                )
                self.modified_canvas.unbind("<Button-1>")

        elif result == 'miss':

            self.mistakes_label.config(
            text=f"Mistakes: {self.state.get_mistakes()} / 3"
            )

            self.status_label.config(
                text=f"Wrong! Mistakes: {self.state.get_mistakes()} / 3",
                fg="red"
            )

            self.root.after(
                2000,
                lambda: self.status_label.config(
                    text="Find the remaining differences!",
                    fg="black"
                )
            )

            if self.state.is_locked():
                messagebox.showwarning(
                    "Too many mistakes",
                    f"You made 3 mistakes.\n"
                    f"You found {self.state.found_count} out of 5."
                )
                self.modified_canvas.unbind("<Button-1>")
             
        elif result == 'already_found':
            self.status_label.config(
                text="Already found that one!",
                fg="orange"
            )
         
        elif result == 'locked':
            self.status_label.config(
                text="No more guesses. Load a new image to play again.",
                fg="darkred"
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = SpotDifferenceGUI(root)
    root.mainloop()
