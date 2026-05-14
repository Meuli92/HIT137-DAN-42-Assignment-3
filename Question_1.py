import tkinter as tk
from GUI_layout import SpotDifferenceGUI


def main():
    """Create the root tkinter window and launch the Spot the Difference game."""
    root = tk.Tk()
    app = SpotDifferenceGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
