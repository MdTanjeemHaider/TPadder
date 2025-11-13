"""Entry point for TPadder GUI application."""
import tkinter as tk
from ui import TPadderApp

if __name__ == "__main__":
    root = tk.Tk()
    app = TPadderApp(root)
    root.mainloop()
