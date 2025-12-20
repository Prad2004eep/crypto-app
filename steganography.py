from PIL import Image
import base64
import zlib

def encode(image_path, secret_message, output_path):
    """
    Encode a secret message into an image using LSB steganography.
    
    Args:
        image_path: Path to the input image
        secret_message: Message to hide in the image
        output_path: Path to save the encoded image
    """
    # Open the image and convert to RGB
    img = Image.open(image_path)
    img = img.convert('RGB')
    
    # Add delimiter to mark end of message
    message = secret_message + '###'
    
    # Convert message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    
    # Get image dimensions
    width, height = img.size
    pixels = img.load()
    
    # Check if message fits in image
    max_bytes = width * height * 3  # 3 channels (R, G, B)
    if len(binary_message) > max_bytes:
        raise ValueError("Message too large for this image")
    
    # Encode message into image
    message_index = 0
    message_length = len(binary_message)
    
    for y in range(height):
        for x in range(width):
            if message_index >= message_length:
                break
                
            r, g, b = pixels[x, y]
            
            # Modify LSB of R channel
            if message_index < message_length:
                # Clear LSB using AND with 11111110, then OR with message bit
                r = (r & 0xFE) | int(binary_message[message_index])
                message_index += 1
            
            # Modify LSB of G channel
            if message_index < message_length:
                g = (g & 0xFE) | int(binary_message[message_index])
                message_index += 1
            
            # Modify LSB of B channel
            if message_index < message_length:
                b = (b & 0xFE) | int(binary_message[message_index])
                message_index += 1
            
            pixels[x, y] = (r, g, b)
        
        if message_index >= message_length:
            break
    
    # Save the encoded image
    img.save(output_path, 'PNG')
    return output_path


def decode(image_path):
    """
    Decode a secret message from an image using LSB steganography.
    
    Args:
        image_path: Path to the encoded image
        
    Returns:
        The decoded secret message
    """
    # Open the image
    img = Image.open(image_path)
    img = img.convert('RGB')
    
    width, height = img.size
    pixels = img.load()
    
    binary_message = ''
    
    # Extract LSBs from image
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            
            # Extract LSB from each channel using AND with 00000001
            binary_message += str(r & 1)
            binary_message += str(g & 1)
            binary_message += str(b & 1)
    
    # Convert binary to text
    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if len(byte) == 8:
            char = chr(int(byte, 2))
            message += char
            
            # Check for delimiter
            if message.endswith('###'):
                return message[:-3]  # Remove delimiter
    
    return message


def encode_audio(image_path, audio_data, output_path):
    """
    Encode audio data into an image using LSB steganography with compression.

    Args:
        image_path: Path to the input image
        audio_data: Binary audio data (bytes)
        output_path: Path to save the encoded image
    """
    # Open the image and convert to RGB
    img = Image.open(image_path)
    img = img.convert('RGB')

    # Compress audio data using zlib (can reduce size by 50-70%)
    compressed_audio = zlib.compress(audio_data, level=9)

    # Store the original size for decompression
    original_size = len(audio_data)
    compressed_size = len(compressed_audio)

    # Create header with sizes (for decompression)
    header = f"{original_size}:{compressed_size}###"
    header_bytes = header.encode('ascii')

    # Combine header and compressed audio
    data_to_encode = header_bytes + compressed_audio

    # Convert to binary bits directly from bytes (more efficient than base64)
    binary_data = ''.join(format(byte, '08b') for byte in data_to_encode)

    # Get image dimensions
    width, height = img.size
    pixels = img.load()

    # Check if audio fits in image
    max_bits = width * height * 3  # 3 channels (R, G, B)
    if len(binary_data) > max_bits:
        max_bytes = max_bits // 8
        current_bytes = len(data_to_encode)
        raise ValueError(f"Audio file too large for this image. Image can store {max_bytes:,} bytes ({max_bytes/1024/1024:.2f} MB), but audio needs {current_bytes:,} bytes ({current_bytes/1024/1024:.2f} MB). Try using a larger image or shorter audio.")

    # Encode audio into image
    data_index = 0
    data_length = len(binary_data)

    for y in range(height):
        for x in range(width):
            if data_index >= data_length:
                break

            r, g, b = pixels[x, y]

            # Modify LSB of R channel
            if data_index < data_length:
                r = (r & 0xFE) | int(binary_data[data_index])
                data_index += 1

            # Modify LSB of G channel
            if data_index < data_length:
                g = (g & 0xFE) | int(binary_data[data_index])
                data_index += 1

            # Modify LSB of B channel
            if data_index < data_length:
                b = (b & 0xFE) | int(binary_data[data_index])
                data_index += 1

            pixels[x, y] = (r, g, b)

        if data_index >= data_length:
            break

    # Save the encoded image
    img.save(output_path, 'PNG')
    return output_path


def decode_audio(image_path):
    """
    Decode compressed audio data from an image using LSB steganography.

    Args:
        image_path: Path to the encoded image

    Returns:
        The decoded audio data as bytes
    """
    # Open the image
    img = Image.open(image_path)
    img = img.convert('RGB')

    width, height = img.size
    pixels = img.load()

    binary_data = ''

    # Extract LSBs from image
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]

            # Extract LSB from each channel using AND with 00000001
            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)

    # Convert binary to bytes
    byte_data = bytearray()
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        if len(byte) == 8:
            byte_data.append(int(byte, 2))

    # Convert to string to find header
    try:
        # Find the header delimiter
        decoded_str = byte_data.decode('ascii', errors='ignore')
        if '###' in decoded_str:
            header_end = decoded_str.index('###')
            header = decoded_str[:header_end]

            # Parse header to get sizes
            if ':' in header:
                parts = header.split(':')
                if len(parts) == 2:
                    original_size = int(parts[0])
                    compressed_size = int(parts[1])

                    # Calculate where compressed data starts
                    header_bytes = (header + '###').encode('ascii')
                    data_start = len(header_bytes)

                    # Extract compressed audio data
                    compressed_audio = bytes(byte_data[data_start:data_start + compressed_size])

                    # Decompress the audio
                    audio_bytes = zlib.decompress(compressed_audio)

                    return audio_bytes
    except Exception as e:
        # Fallback: try old base64 format for backward compatibility
        try:
            decoded_text = ''
            for i in range(0, len(binary_data), 8):
                byte = binary_data[i:i+8]
                if len(byte) == 8:
                    try:
                        char = chr(int(byte, 2))
                        decoded_text += char

                        if decoded_text.endswith('###END###'):
                            decoded_text = decoded_text[:-9]
                            if '###' in decoded_text:
                                parts = decoded_text.split('###', 1)
                                if len(parts) == 2:
                                    audio_b64 = parts[1]
                                    audio_bytes = base64.b64decode(audio_b64)
                                    return audio_bytes
                    except (ValueError, UnicodeDecodeError):
                        continue
        except:
            pass

    raise ValueError("No valid audio data found in image")


