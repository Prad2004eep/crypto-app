# LSB Steganography Web App

Hide secret messages and voice recordings in images using Least Significant Bit (LSB) steganography.

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Open browser at `http://localhost:5000`

## Features

### Text Steganography
**Encode:** Upload image → Enter message → Download encoded image
**Decode:** Upload encoded image → View hidden message

### Audio Steganography (NEW!)
**Encode:** Upload image → Record/Upload audio → Download encoded image
**Decode:** Upload encoded image → Download hidden audio

## Tips

- Use PNG format for best results (lossless)
- Larger images can store longer messages/audio
- Audio is automatically compressed (50-70% size reduction)
- **Storage Capacity:**
  - 1920x1080 (Full HD): ~0.74 MB
  - 3840x2160 (4K): ~3 MB
  - 7680x4320 (8K): ~12 MB
  - 10000x10000: ~36 MB
  - 20000x20000: ~143 MB
- Record audio directly in browser or upload existing files
- Max file size: 1000MB (1GB)

## Create Large Images for Long Audio

For storing long audio recordings, create a large blank image:

```bash
python create_large_image.py
`

This will help you generate images with sufficient storage capacity.

