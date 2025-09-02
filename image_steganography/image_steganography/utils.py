from PIL import Image
import hashlib


def encode_message(image_path, message, key):
    """
    Encodes a secret message into an image using Least Significant Bit (LSB) encoding.
    """
    try:
        # Open the image
        img = Image.open(image_path)
        pixels = img.load()  # Get the pixel data

        # Prepare the message with a separator for the key
        encoded_message = message + "||" + hashlib.sha256(key.encode()).hexdigest()

        # Ensure the message fits into the image
        if len(encoded_message) * 8 > img.width * img.height:
            raise ValueError("Message is too large to fit in the image.")

        message_bin = ''.join(format(ord(c), '08b') for c in encoded_message)  # Convert message to binary
        data_index = 0  # Track the current position in the binary data

        # Encode the message into the image's pixels (LSB method)
        for y in range(img.height):
            for x in range(img.width):
                if data_index < len(message_bin):
                    pixel = list(pixels[x, y])  # Get the pixel (R, G, B)
                    # Modify the least significant bit (LSB) of each color channel to store the message
                    for i in range(3):  # Modify R, G, and B channels
                        if data_index < len(message_bin):
                            pixel[i] = (pixel[i] & ~1) | int(message_bin[data_index])
                            data_index += 1
                    pixels[x, y] = tuple(pixel)  # Update the pixel

        # Return the modified image
        return img

    except Exception as e:
        raise ValueError(f"Encoding failed: {e}")


def decode_message(image_path, key):
    """
    Decodes a secret message from an image.
    """
    try:
        img = Image.open(image_path)
        pixels = img.load()

        # Extract the binary data from the image
        binary_data = ""
        for y in range(img.height):
            for x in range(img.width):
                pixel = pixels[x, y]
                for i in range(3):  # Check R, G, and B channels
                    binary_data += str(pixel[i] & 1)  # Get LSB

        # Convert the binary data into a string
        decoded_message = ""
        for i in range(0, len(binary_data), 8):
            byte = binary_data[i:i+8]
            decoded_message += chr(int(byte, 2))

        # The message and key are separated by '||'
        message_parts = decoded_message.split("||")
        if len(message_parts) < 2:
            raise ValueError("No valid message found.")
        
        return message_parts[0]  # Return the original secret message

    except Exception as e:
        raise ValueError(f"Decoding failed: {e}")


def save_image_with_message(image, save_path):
    """
    Saves the encoded image to a file.
    """
    try:
        image.save(save_path)
    except Exception as e:
        raise ValueError(f"Error saving image: {e}")
