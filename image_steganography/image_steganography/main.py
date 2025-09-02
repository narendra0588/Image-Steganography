import tkinter as tk
from encode import open_encode_screen
from decode import open_decode_screen


def main_screen():
    root = tk.Tk()
    root.title("Image Steganography")
    root.geometry("800x600")
    
    # Add background image
    from PIL import Image, ImageTk
    bg_image = Image.open("assets/background.jpeg")  # Ensure the path is correct and the file exists
    bg_image = bg_image.resize((800, 600), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)


    # Buttons
    encode_button = tk.Button(
        root, text="Encode", command=lambda: open_encode_screen(root), width=15, height=2, font=("Helvetica", 14), bg="#80deea"
    )
    decode_button = tk.Button(
        root, text="Decode", command=lambda: open_decode_screen(root), width=15, height=2, font=("Helvetica", 14), bg="#80deea"
    )
    encode_button.pack(side=tk.LEFT, padx=100, pady=200)
    decode_button.pack(side=tk.RIGHT, padx=100, pady=200)

    root.mainloop()


if __name__ == "__main__":
    main_screen()
