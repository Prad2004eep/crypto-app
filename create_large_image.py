"""
Helper script to create large blank images for storing long audio recordings
"""
from PIL import Image
import sys

def create_blank_image(width, height, output_path='large_image.png', color=(255, 255, 255)):
    """
    Create a large blank image for audio steganography
    
    Args:
        width: Image width in pixels
        height: Image height in pixels
        output_path: Where to save the image
        color: RGB color tuple (default: white)
    """
    # Calculate storage capacity
    total_bytes = (width * height * 3) // 8
    total_mb = total_bytes / (1024 * 1024)
    
    print(f"Creating {width}x{height} image...")
    print(f"Storage capacity: {total_mb:.2f} MB ({total_bytes:,} bytes)")
    
    # Create the image
    img = Image.new('RGB', (width, height), color)
    
    # Save as PNG
    img.save(output_path, 'PNG')
    print(f"✓ Image saved to: {output_path}")
    print(f"\nYou can now use this image to encode audio files up to {total_mb:.2f} MB")

if __name__ == '__main__':
    print("=" * 70)
    print("LARGE IMAGE GENERATOR FOR AUDIO STEGANOGRAPHY")
    print("=" * 70)
    print()
    
    # Predefined sizes
    sizes = {
        '1': (5000, 5000, 'large_5k.png', '~9 MB storage'),
        '2': (10000, 10000, 'large_10k.png', '~36 MB storage'),
        '3': (15000, 15000, 'large_15k.png', '~81 MB storage'),
        '4': (20000, 20000, 'large_20k.png', '~143 MB storage'),
    }
    
    print("Select image size:")
    for key, (w, h, name, capacity) in sizes.items():
        print(f"  {key}. {w}x{h} pixels - {capacity}")
    print("  5. Custom size")
    print()
    
    choice = input("Enter choice (1-5): ").strip()
    
    if choice in sizes:
        width, height, output_path, _ = sizes[choice]
        create_blank_image(width, height, output_path)
    elif choice == '5':
        try:
            width = int(input("Enter width (pixels): "))
            height = int(input("Enter height (pixels): "))
            output_path = input("Enter output filename (default: large_image.png): ").strip()
            if not output_path:
                output_path = 'large_image.png'
            create_blank_image(width, height, output_path)
        except ValueError:
            print("Error: Invalid input. Please enter numbers only.")
    else:
        print("Invalid choice!")
    
    print()
    print("=" * 70)

