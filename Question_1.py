import tkinter as tk
from GUI_layout import SpotDifferenceGUI

def main():
    root = tk.Tk()
    app = SpotDifferenceGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()