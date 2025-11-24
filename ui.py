"""User interface implementation for TPadder."""
import os
import tkinter as tk
from tkinter import filedialog, font, colorchooser
from PIL import Image
import image_processor as ip

# Constants
PREVIEW_SIZE_MAX = (512, 512)

class TPadderUI:
    """Main UI class for TPadder application."""

    def __init__(self, root):
        """Initialize the main UI components and variables."""
        self.main = tk.Frame(root)
        self.main.pack(fill="both", expand=True)

        # Variables
        self.images = []  # List of tuples: (original, padded, highlighted, file_name)
        self.image_previews = []  # List of Tkinter PhotoImages for previews
        self.current_image_index = 0
        self.source_paths = tk.StringVar()
        self.need_highlight = tk.BooleanVar(value=False)
        self.highlight_color = (255, 255, 255, 255)
        self.color_display = None
        self.preview_frame = None
        self.save_button = None
        self.status_label = None

        self.build_ui()


    def build_ui(self):
        """Build the full user interface layout."""
        self.build_source_selection()
        self.build_highlight_options()
        self.build_preview_area()
        self.build_save_options()
        self.build_status_bar()

        self.update_status("Waiting for image selection...", "idle")


    def build_source_selection(self):
        """Build the UI elements for selecting image files."""
        frame = tk.Frame(self.main)
        frame.pack(fill="x", padx=5, pady=2)

        title_font = font.Font(size=10, weight="bold")
        tk.Label(frame, text="Select Image(s) (PNG):", font=title_font).pack(side=tk.LEFT)

        tk.Entry(frame, textvariable=self.source_paths, state="readonly").pack(
            side=tk.LEFT, fill="x", expand=True, padx=2
        )

        tk.Button(frame, text="Browse", command=self.browse_files).pack(
            side=tk.LEFT,
            padx=2
        )


    def build_highlight_options(self):
        """Build the UI elements for highlight options."""
        frame = tk.Frame(self.main)
        frame.pack(fill="x", pady=2, padx=5)

        tk.Checkbutton(
            frame,
            text="Save Highlighted Texture",
            variable=self.need_highlight
        ).pack(side=tk.TOP)

        # Color chooser
        color_choice_frame = tk.Frame(frame)
        color_choice_frame.pack()
        tk.Label(color_choice_frame, text="Highlight Color (white recommended):").pack(
            side=tk.LEFT
        )

        self.color_display = tk.Button(
            color_choice_frame,
            width=3,
            relief="solid",
            borderwidth=1,
            bg="white",
            command=self.choose_highlight_color
        )
        self.color_display.pack(side=tk.LEFT)


    def build_preview_area(self):
        """Create the frame to display image previews."""
        self.preview_frame = tk.Frame(self.main)
        self.preview_frame.pack(fill="both", expand=True, pady=5)


    def build_save_options(self):
        """Create the save button for saving processed images."""
        frame = tk.Frame(self.main)
        frame.pack(pady=5)

        self.save_button = tk.Button(frame, text="Save", command=self.save, width=8)
        self.save_button.config(state="disabled")
        self.save_button.pack(side=tk.LEFT, padx=5)


    def build_status_bar(self):
        """Create a status bar to display messages to the user."""
        tk.Frame(self.main, height=1, bg="black").pack(fill="x", side="top")
        self.status_label = tk.Label(self.main, anchor="center")
        self.status_label.pack(fill="x")


    def browse_files(self):
        """Open file dialog to select PNG files."""
        paths = filedialog.askopenfilenames(
            title="Select Image Files",
            filetypes=[("PNG Images", "*.png")],
        )

        if not paths:
            return

        if len(paths) == 1:
            self.source_paths.set(paths[0])
        else:
            self.source_paths.set(f"{len(paths)} files selected")

        self.load_images(paths)


    def load_images(self, paths):
        """Load images from the selected file paths"""
        total = len(paths)
        failures = []

        self.update_status(f"Loading {total} image(s)...", "pending")
        self.current_image_index = 0
        self.images.clear()

        # Load each image and create padded/highlighted versions
        for i, path in enumerate(paths, start=1):
            original = Image.open(path)

            if not ip.is_valid_image(original):
                failures.append(path)
                continue

            padded = ip.convert(original)
            highlighted = ip.convert_highlighted(padded, self.highlight_color)
            file_name = os.path.basename(path)
            self.images.append((original, padded, highlighted, file_name))
            self.update_status(f"Loaded {i}/{total} image(s)", "success")
            self.main.update_idletasks()

        if not self.images:
            self.update_status(
                "No valid images loaded. Ensure files are valid PNG with transparency.", "error"
            )
            self.save_button.config(state="disabled")
            return

        self.save_button.config(state="normal")
        self.create_previews()
        self.display_previews()

        if failures:
            self.update_status(
                f"Loaded {len(self.images)}/{total}. {len(failures)} failed.",
                "error"
            )
        else:
            self.update_status(f"Loaded {total}/{total} image(s).", "success")


    def display_previews(self):
        """Display image previews in the preview area."""
        # Clear previous previews
        for widget in self.preview_frame.winfo_children():
            widget.destroy()

        columns_frame = tk.Frame(self.preview_frame)
        columns_frame.pack(fill="both", expand=True, pady=5)

        titles = ["Original", "Padded", "Highlighted"]
        images = self.image_previews[self.current_image_index]
        title_font = font.Font(weight="bold")

        for title, image in zip(titles, images):
            column_frame = tk.Frame(columns_frame)
            column_frame.pack(side=tk.LEFT, expand=True, padx=10)
            tk.Label(
                column_frame,
                text=title,
                font=title_font,
                bg="gray",
                image=image,
                compound="bottom"
            ).pack(expand=True, fill="both")

        self.build_navigation_controls()


    def build_navigation_controls(self):
        """Create navigation buttons to move between images."""
        nav_frame = tk.Frame(self.preview_frame)
        nav_frame.pack()

        previous_button = tk.Button(
            nav_frame, text="◀ Previous",
            command=self.previous_image,
            width=10
        )
        previous_button.pack(side=tk.LEFT, padx=5)
        tk.Label(
            nav_frame,
            text=f"{self.current_image_index + 1} / {len(self.images)}"
        ).pack(side=tk.LEFT, padx=5)
        next_button = tk.Button(nav_frame, text="Next ▶", command=self.next_image, width=10)
        next_button.pack(side=tk.LEFT, padx=5)

        # Disable buttons based on position
        if self.current_image_index == 0:
            previous_button.config(state="disabled")
        if self.current_image_index == len(self.images) - 1:
            next_button.config(state="disabled")


    def previous_image(self):
        """Display the previous image in the list."""
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.display_previews()


    def next_image(self):
        """Display the next image in the list."""
        if self.current_image_index < len(self.images) - 1:
            self.current_image_index += 1
            self.display_previews()


    def create_previews(self):
        """Generate thumbnail previews for all loaded images."""
        self.image_previews.clear()
        for original, padded, highlighted, _ in self.images:
            self.image_previews.append(
                (
                    ip.create_thumbnail(original, PREVIEW_SIZE_MAX),
                    ip.create_thumbnail(padded, PREVIEW_SIZE_MAX),
                    ip.create_thumbnail(highlighted, PREVIEW_SIZE_MAX),
                )
            )


    def update_status(self, message, code):
        """Update the status label with a message and color."""
        colors = {
            "idle": "gray",
            "pending": "orange",
            "success": "green",
            "error": "red",
        }

        self.status_label.config(text=message, fg=colors.get(code, "black"))


    def choose_highlight_color(self):
        """Open color chooser dialog and update highlight color."""
        color_code = colorchooser.askcolor(title="Choose Highlight Color (white recommended)")
        if not color_code[0]:
            return

        self.highlight_color = tuple(map(int, color_code[0]))
        self.color_display.config(bg=color_code[1])

        if self.images:
            for i, (original, padded, _, file_name) in enumerate(self.images):
                new_highlighted = ip.convert_highlighted(original, self.highlight_color)
                self.images[i] = (original, padded, new_highlighted, file_name)
            self.create_previews()
            self.display_previews()


    def save(self):
        """Save the padded and optionally highlighted images to a directory."""
        directory = filedialog.askdirectory(title="Select Directory to Save Images")
        if not directory:
            return

        for _, padded_image, highlighted_image, file_name in self.images:
            padded_image.save(os.path.join(directory, file_name))
            if self.need_highlight.get():
                highlighted_image.save(os.path.join(directory, file_name[:-4] + "_Highlighted.png"))

        self.update_status(f"Saved image(s) to: {directory}", "success")
