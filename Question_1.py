import tkinter as tk
from game_window import GameWindow

def main():
    root = tk.Tk()
    root.title("Spot the Difference")
    app = GameWindow(root)
    app.setup_layout()
    root.mainloop()

if __name__ == "__Question_1__":
    main()
