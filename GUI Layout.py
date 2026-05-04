class SpotDifferenceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Spot the Difference Game")
        self.root.geometry("1100x700")
        self.root.resizable(False, False)

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
            self.status_label.config(text="Image loaded successfully.")
            messagebox.showinfo("Image Loaded", "Image has been loaded.")

    def reveal_differences(self):
        self.status_label.config(text="Revealing all differences.")
        messagebox.showinfo("Reveal", "Reveal function will be added later.")

    def restart_game(self):
        self.remaining_label.config(text="Remaining Differences: 5")
        self.mistakes_label.config(text="Mistakes: 0 / 3")
        self.status_label.config(text="Game restarted.")
        self.original_canvas.delete("all")
        self.modified_canvas.delete("all")

    def check_click(self, event):
        x = event.x
        y = event.y
        self.status_label.config(text=f"Clicked at: ({x}, {y})")


if __name__ == "__main__":
    root = tk.Tk()
    app = SpotDifferenceGUI(root)
    root.mainloop()
