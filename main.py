"""Entry point for TPadder GUI application."""
import os
import sys
import tkinter as tk
from ui import TPadderUI

ICONPATH = os.path.join(
    getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))),
    "Icons/icon.ico"
)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("TPadder - v3.0")
    root.iconbitmap(ICONPATH)
    app = TPadderUI(root)
    root.mainloop()
