"""
Test script to calculate audio storage capacity for different image sizes
"""

def calculate_capacity(width, height):
    """Calculate how much audio data can be stored in an image"""
    # Total pixels
    total_pixels = width * height
    
    # Each pixel has 3 channels (R, G, B), each can store 1 bit
    total_bits = total_pixels * 3
    
    # Convert to bytes
    total_bytes = total_bits // 8
    
    # Convert to MB
    total_mb = total_bytes / (1024 * 1024)
    
    # Estimate audio duration (assuming ~1MB per minute for compressed audio)
    # WAV audio is typically 10MB per minute, but with compression (50-70% reduction)
    # we get approximately 3-5MB per minute
    min_minutes = total_mb / 5  # Conservative estimate
    max_minutes = total_mb / 3  # Optimistic estimate
    
    return {
        'resolution': f'{width}x{height}',
        'total_bytes': total_bytes,
        'total_mb': total_mb,
        'min_minutes': min_minutes,
        'max_minutes': max_minutes
    }

# Common image resolutions
resolutions = [
    (1920, 1080),   # Full HD
    (2560, 1440),   # 2K
    (3840, 2160),   # 4K
    (7680, 4320),   # 8K
]

print("=" * 70)
print("AUDIO STORAGE CAPACITY WITH COMPRESSION")
print("=" * 70)
print()

for width, height in resolutions:
    result = calculate_capacity(width, height)
    print(f"Resolution: {result['resolution']}")
    print(f"  Storage: {result['total_mb']:.2f} MB ({result['total_bytes']:,} bytes)")
    print(f"  Audio Duration: {result['min_minutes']:.1f} - {result['max_minutes']:.1f} minutes")
    print()

print("=" * 70)
print("Note: Actual duration depends on audio quality and compression ratio")
print("=" * 70)

