import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageCaptionTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Captioning Tool")

        self.current_index = 0
        self.image_files = []
        self.text_files = []

        self.image_label = tk.Label(root)
        self.image_label.pack()

        self.text_entry = tk.Text(root, wrap=tk.WORD, width=60, height=10)
        self.text_entry.pack()

        self.load_button = tk.Button(root, text="Load Folder", command=self.load_folder)
        self.load_button.pack()

        self.prev_button = tk.Button(root, text="Previous", command=self.load_previous, state=tk.DISABLED)
        self.prev_button.pack(side=tk.LEFT)

        self.next_button = tk.Button(root, text="Next", command=self.load_next, state=tk.DISABLED)
        self.next_button.pack(side=tk.RIGHT)

        self.root.bind("<Alt-Left>", self.load_previous)
        self.root.bind("<Alt-Right>", self.load_next)

    def load_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.image_files, self.text_files = self.get_image_and_text_files(folder_path)
            if self.image_files:
                self.current_index = 0
                self.load_image_and_text()

    def get_image_and_text_files(self, folder_path):
        image_files = []
        text_files = []

        for filename in os.listdir(folder_path):
            if filename.lower().endswith(".png"):
                image_files.append(os.path.join(folder_path, filename))
            elif filename.lower().endswith(".txt"):
                text_files.append(os.path.join(folder_path, filename))

        # Sort the lists to ensure matching pairs
        image_files.sort()
        text_files.sort()

        return image_files, text_files

    def load_image_and_text(self):
        if 0 <= self.current_index < len(self.image_files):
            image_path = self.image_files[self.current_index]
            text_path = self.text_files[self.current_index]

            # Load and display the image
            image = Image.open(image_path)
            image.thumbnail((512, 512))
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.photo = photo

            # Load and display the text
            if os.path.exists(text_path):
                with open(text_path, 'r') as text_file:
                    text = text_file.read()
                    self.text_entry.delete('1.0', tk.END)
                    self.text_entry.insert(tk.END, text)
            else:
                # Only clear the text if the text file does not exist
                self.text_entry.delete('1.0', tk.END)

            # Enable navigation buttons
            self.prev_button.config(state=tk.NORMAL if self.current_index > 0 else tk.DISABLED)
            self.next_button.config(state=tk.NORMAL if self.current_index < len(self.image_files) - 1 else tk.DISABLED)

            # Set focus to the text entry
            self.text_entry.focus()

    def save_text(self):
        if 0 <= self.current_index < len(self.text_files):
            text_path = self.text_files[self.current_index]
            edited_text = self.text_entry.get('1.0', tk.END)
            with open(text_path, 'w') as text_file:
                text_file.write(edited_text)

    def load_previous(self, event=None):
        # Save the edited text before switching to the previous pair
        self.save_text()

        if self.current_index > 0:
            self.current_index -= 1
        else:
            # Loop to the last image if at the first image
            self.current_index = len(self.image_files) - 1
        self.load_image_and_text()

    def load_next(self, event=None):
        # Save the edited text before switching to the next pair
        self.save_text()

        if self.current_index < len(self.image_files) - 1:
            self.current_index += 1
        else:
            # Loop to the first image if at the last image
            self.current_index = 0
        self.load_image_and_text()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCaptionTool(root)
    root.mainloop()
