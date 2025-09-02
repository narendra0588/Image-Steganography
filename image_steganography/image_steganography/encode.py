import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from utils import encode_message, save_image_with_message


def open_encode_screen(root):
    root.withdraw()
    encode_screen = tk.Toplevel()
    encode_screen.title("Encode Message")
    encode_screen.geometry("800x600")

    # Back button
    back_button = tk.Button(
        encode_screen, text="Back", command=lambda: go_back(encode_screen, root), width=10
    )
    back_button.place(x=10, y=10)

    # Image area
    image_label = tk.Label(
        encode_screen,
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
                image_label.file_path = file_path  # Save the file path for encoding
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {e}")

    upload_button = tk.Button(encode_screen, text="Upload Image", command=upload_image)
    upload_button.place(x=65, y=380)

    # Text area
    text_box = tk.Text(encode_screen, width=40, height=18)
    text_box.insert(tk.END, "Type your secret message here...")
    text_box.bind("<FocusIn>", lambda e: text_box.delete("1.0", tk.END))
    text_box.place(x=400, y=50)

    # Clear Text button
    def clear_text():
        text_box.delete("1.0", tk.END)

    clear_text_button = tk.Button(encode_screen, text="Clear Text", command=clear_text)
    clear_text_button.place(x=600, y=380)

    # Encrypt button
    def encrypt_message():
        if not hasattr(image_label, "file_path"):
            messagebox.showerror("Error", "Please upload an image first!")
            return
        message = text_box.get("1.0", tk.END).strip()
        if not message:
            messagebox.showerror("Error", "Please enter a secret message!")
            return
        
        secret_key = get_secret_key()  # Wait for the secret key to be entered
        if not secret_key:
            return
        
        try:
            # Encode the message into the image
            encoded_image = encode_message(image_label.file_path, message, secret_key)
            save_path = filedialog.asksaveasfilename(
                defaultextension=".png", filetypes=[("PNG Files", "*.png")]
            )
            if save_path:
                save_image_with_message(encoded_image, save_path)
                messagebox.showinfo("Success", "Message encrypted and image saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {e}")

    encrypt_button = tk.Button(encode_screen, text="Encrypt", command=encrypt_message)
    encrypt_button.place(x=450, y=380)


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
