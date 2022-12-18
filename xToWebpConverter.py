from pathlib import Path
from PIL import Image

import tkinter as tk
import threading
from tkinter import filedialog
from tkinter import ttk


options = ['png', 'jpg']
current_format = options[0]


def selection_changed(event):
    global current_format
    current_format = combo.get()


def select_file():
    filepath = filedialog.askdirectory()
    filepath_label.config(text=filepath)
    print(f"Selected file: {filepath}")


def select_file2():
    filepath = filedialog.askdirectory()
    filepath_label2.config(text=filepath)
    print(f"Selected file: {filepath}")


def convert_to_webp(source, destination=None):
    """Convert image to WebP.

    Args:
        source (pathlib.Path): Path to source image
        destination (pathlib.Path): Path to Folder

    Returns:
        pathlib.Path: path to new image
    """
    if destination is None:
        destination = source.with_suffix(".webp")
    elif destination.is_dir():
        destination = destination / source.name

    image = Image.open(source)  # Open image
    image.save(destination, format="webp")  # Convert image to webp

    return destination


def generate_webp():
    paths = list(Path(filepath_label.cget('text')).glob(F"**/*.{current_format}"))
    for i, path in enumerate(paths):
        file_label.config(text=path.name)
        progress["value"] = (i / len(paths)) * 100
        root.update()
        webp_path = convert_to_webp(path, Path(filepath_label2.cget('text')))
        print(webp_path)
    progress["value"] = 100
    root.update()


def new_thread():
    thread = threading.Thread(target=generate_webp)
    thread.start()


root = tk.Tk()
root.wm_title("* to webp Converter")

i_des_label = tk.Label(root, text="Inputpath:")
i_des_label.grid(row=0, column=0)

filepath_label = tk.Label(root, text="No file selected")
filepath_label.grid(row=0, column=1)

button = tk.Button(root, text="Select file", command=select_file)
button.grid(row=0, column=2)

i_des_label1 = tk.Label(root, text="Outputpath:")
i_des_label1.grid(row=1, column=0)

filepath_label2 = tk.Label(root, text="No file selected")
filepath_label2.grid(row=1, column=1)

button2 = tk.Button(root, text="Select file", command=select_file2)
button2.grid(row=1, column=2)

i_des_label1 = tk.Label(root, text="Imageformat: ")
i_des_label1.grid(row=3, column=0)

combo = ttk.Combobox(root, values=options, state="readonly")
combo.bind("<<ComboboxSelected>>", selection_changed)
combo.set(current_format)
combo.grid(row=3, column=1)

progress = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
progress.grid(row=4, column=1)

file_label =  tk.Label(root, text="--")
file_label.grid(row=4, column=2)

button = tk.Button(root, text="Generate", command=new_thread)
button.grid(row=4, column=0)

root.mainloop()


if __name__ == '__main__':
    print('go')

