import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from utils import decode_message


def open_decode_screen(root):
    root.withdraw()
    decode_screen = tk.Toplevel()
    decode_screen.title("Decode Message")
    decode_screen.geometry("800x600")

    # Back button
    back_button = tk.Button(
        decode_screen, text="Back", command=lambda: go_back(decode_screen, root), width=10
    )
    back_button.place(x=10, y=10)

    # Image area
    image_label = tk.Label(
        decode_screen,
        text="Your image will appear here",
        bg="#f0f0f0",
        relief=tk.SUNKEN
    )
    image_label.place(x=50, y=50, width=300, height=300)  # Fixed 300x300 area for image display

    # Upload Image button
    def upload_image():
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            try:
                img = Image.open(file_path)
                # Resize to fit within 300x300 while maintaining aspect ratio
                img.thumbnail((300, 300), Image.LANCZOS)
                img = ImageTk.PhotoImage(img)
                image_label.config(image=img, text="")  # Clear placeholder text
                image_label.image = img  # Keep a reference to prevent garbage collection
                image_label.file_path = file_path  # Save the file path for decoding
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {e}")

    upload_button = tk.Button(decode_screen, text="Upload Image", command=upload_image)
    upload_button.place(x=65, y=380)

    # Decrypt button
    def decrypt_message():
        if not hasattr(image_label, "file_path"):
            messagebox.showerror("Error", "Please upload an image first!")
            return

        secret_key = get_secret_key()  # Wait for the secret key to be entered
        if not secret_key:
            return

        try:
            # Decode the message from the image
            decoded_message = decode_message(image_label.file_path, secret_key)
            messagebox.showinfo("Decoded Message", decoded_message)
        except Exception as e:
            messagebox.showerror("Error", f"Decoding failed: {e}")

    decrypt_button = tk.Button(decode_screen, text="Decrypt", command=decrypt_message)
    decrypt_button.place(x=450, y=380)


def get_secret_key():
    key_screen = tk.Toplevel()
    key_screen.geometry("300x150")
    key_screen.title("Enter Secret Key")

    key_label = tk.Label(key_screen, text="Enter your secret key:")
    key_label.pack(pady=10)

    key_entry = tk.Entry(key_screen, show="*")
    key_entry.pack(pady=5)

    secret_key = tk.StringVar()

    def submit_key():
        secret_key.set(key_entry.get())
        key_screen.destroy()

    submit_button = tk.Button(key_screen, text="Submit", command=submit_key)
    submit_button.pack(pady=10)

    key_screen.wait_window(key_screen)  # This ensures that the main loop waits until the window is closed

    return secret_key.get()  # Return the secret key entered by the user


def go_back(current_screen, root):
    current_screen.destroy()
    root.deiconify()
