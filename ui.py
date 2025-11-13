"""User interface implementation for TPadder"""
import os
import sys
import tkinter as tk
from tkinter import filedialog, font, colorchooser
from PIL import Image, ImageTk
import utils

ICONPATH = os.path.join(
    getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))),
    "Icons/icon.ico"
)


class TPadderApp:
    """Main application class for TPadder GUI."""

    def __init__(self, window):
        self.window = window
        self.window.title("TPadder - v2.0")
        self.window.iconbitmap(ICONPATH)
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)

        # Variables
        self.source_path = tk.StringVar()
        self.highlight_color = (255, 255, 255, 255)
        self.source_image = None
        self.padded_image = None
        self.highlighted_image = None
        self.source_preview = None
        self.padded_preview = None
        self.highlighted_preview = None
        self.source_preview_label = None
        self.padded_preview_label = None
        self.highlighted_preview_label = None
        self.need_highlight = tk.BooleanVar(value=False)

        # Build UI
        self.build_ui()


    def build_ui(self):
        """Build the Tkinter UI."""

        title_font = font.Font(size=10, weight="bold")

        # Main container
        main_container = tk.Frame(self.window)
        main_container.grid(row=0, column=0, sticky="nsew")
        main_container.rowconfigure(2, weight=1)
        main_container.columnconfigure(0, weight=1)

        # Source selection container
        tk.Label(main_container, text="Source Texture (PNG):", font=title_font).pack(
            pady=2
        )
        path_container = tk.Frame(main_container)
        path_container.pack(fill="x", pady=2)
        tk.Entry(path_container, textvariable=self.source_path).pack(
            side=tk.LEFT, fill="x", expand=True, padx=5
        )
        tk.Button(path_container, text="Browse", command=self.browse_source).pack(
            side=tk.LEFT, padx=5
        )

        # Highlight color selection container
        color_container = tk.Frame(main_container)
        color_container.pack(pady=2)
        tk.Label(color_container, text="Highlight Color (white recommended):").pack(
            side=tk.LEFT, padx=5
        )
        self.color_display = tk.Label(
            color_container,
            bg="white", width=3,
            borderwidth=1,
            relief="solid"
        )
        self.color_display.pack(side=tk.LEFT, padx=5)
        tk.Button(color_container, text="Choose", command=self.choose_highlight_color).pack(
            side=tk.LEFT, padx=5
        )

        # Preview area container
        self.preview_container = tk.Frame(main_container)
        self.preview_container.pack(fill="both", expand=True, pady=2)
        for i in range(3):
            self.preview_container.columnconfigure(i, weight=1)

        # Save options container
        self.save_container = tk.Frame(main_container)
        self.save_container.pack(pady=5)
        self.save_check = tk.Checkbutton(
            self.save_container,
            text="Save Highlighted Texture",
            variable=self.need_highlight
        )
        self.save_check.pack(side=tk.LEFT, padx=5)
        self.save_button = tk.Button(self.save_container, text="Save", command=self.save)
        self.save_button.pack(side=tk.LEFT, padx=5)
        self.save_check.config(state="disabled")
        self.save_button.config(state="disabled")

        # Status label
        tk.Frame(main_container, height=1, bg="black").pack(fill="x", side="top")
        self.status_label = tk.Label(main_container, text="Ready", anchor="center")
        self.status_label.pack(fill="x")
        self.update_status("Waiting for input...", "idle")


    def browse_source(self):
        """Open file dialog to select a source image."""

        path = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png")])
        if path:
            self.source_path.set(path)
            self.load_preview()


    def load_preview(self):
        """Load and display previews of the original, padded, and highlighted images."""

        path = self.source_path.get()

        try:
            self.source_image = Image.open(path)
            self.padded_image = utils.convert(self.source_image)
            self.highlighted_image = utils.convert_highlighted(self.source_image, self.highlight_color)
        except Exception as e:
            self.update_status(
                f"Unable to load image: {e}. Ensure it is a valid PNG file with transparency.",
                "error"
            )
            return

        if self.source_preview_label is None:
            self.create_preview_labels()

        self.source_preview = ImageTk.PhotoImage(self.source_image)
        self.padded_preview = ImageTk.PhotoImage(self.padded_image)
        self.highlighted_preview = ImageTk.PhotoImage(self.highlighted_image)

        self.source_preview_label.config(image=self.source_preview)
        self.padded_preview_label.config(image=self.padded_preview)
        self.highlighted_preview_label.config(image=self.highlighted_preview)

        self.save_check.config(state="normal")
        self.save_button.config(state="normal")
        self.update_status("Preview loaded. Ready to save.", "success")


    def create_preview_labels(self):
        """Create preview labels for original, padded, and highlighted images."""

        tk.Label(self.preview_container, text="Original").grid(row=0, column=0)
        tk.Label(self.preview_container, text="Padded").grid(row=0, column=1)
        tk.Label(self.preview_container, text="Highlighted").grid(row=0, column=2)

        self.source_preview_label = tk.Label(self.preview_container, bg="gray")
        self.padded_preview_label = tk.Label(self.preview_container, bg="gray")
        self.highlighted_preview_label = tk.Label(self.preview_container, bg="gray")

        self.source_preview_label.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.padded_preview_label.grid(row=1, column=1, sticky="nsew", padx=10, pady=5)
        self.highlighted_preview_label.grid(row=1, column=2, sticky="nsew", padx=10, pady=5)


    def choose_highlight_color(self):
        """Open color chooser dialog to select highlight color."""

        color_code = colorchooser.askcolor(
            title="Choose Highlight Color (white recommended)"
        )

        if color_code[0]:
            self.highlight_color = tuple(map(int, color_code[0]))
            self.color_display.config(bg=color_code[1])
            if self.source_path.get():
                self.load_preview()


    def save(self):
        """Save the padded image and optional highlighted image."""

        if not self.padded_image:
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".png", filetypes=[("PNG Files", "*.png")]
        )

        if not path:
            return

        self.padded_image.save(path)
        if self.need_highlight.get():
            self.highlighted_image.save(path[:-4] + "_Highlighted.png")
            self.update_status(f"Saved to: {path} and {path[:-4]}_Highlighted.png", "success")
        else:
            self.update_status(f"Saved to: {path}", "success")


    def update_status(self, message, code):
        """Update the status label with message and color based on code."""

        match code:
            case "idle":
                self.status_label.config(text=message, fg="gray")
            case "success":
                self.status_label.config(text=message, fg="green")
            case "error":
                self.status_label.config(text=message, fg="red")
