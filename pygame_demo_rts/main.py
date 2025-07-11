import sys
import bluetooth
from PIL import Image
import numpy as np

def convert_image_to_escpos_raster(filepath, width=384, dither=False):
    # Load RGBA image and separate alpha mask
    img_rgba = Image.open(filepath).convert("RGBA")
    alpha = img_rgba.getchannel("A")

    # Flatten onto white background
    white_bg = Image.new("RGBA", img_rgba.size, (255, 255, 255, 255))
    flattened = Image.alpha_composite(white_bg, img_rgba).convert("L")

    # Resize both image and alpha mask
    height = int(flattened.height * (width / flattened.width))
    img_resized = flattened.resize((width, height), Image.Resampling.LANCZOS)
    alpha_resized = alpha.resize((width, height), Image.Resampling.LANCZOS)

    # Convert alpha to numpy for masking
    alpha_mask = np.array(alpha_resized, dtype=np.uint8)
    img_array = np.array(img_resized, dtype=np.uint8)

    # Apply alpha mask BEFORE dithering - set transparent areas to white
    img_array[alpha_mask < 128] = 255

    # Convert back to PIL Image for dithering/thresholding
    img_masked = Image.fromarray(img_array, mode="L")

    # Apply dither or threshold
    if dither:
        from PIL.Image import Dither
        img_bw = img_masked.convert("1", dither=Dither.FLOYDSTEINBERG)
    else:
        img_bw = img_masked.point(lambda x: 0 if x < 128 else 255, mode="1")

    # Convert to NumPy for final processing
    bits = np.array(img_bw, dtype=np.uint8)

    # Invert bits for ESC/POS format (0=black, 1=white)
    # PIL's mode "1" gives us 0=black, 255=white
    # But we need 0=white, 1=black for packbits
    bits_inverted = (bits == 0).astype(np.uint8)

    # Pack bits into bytes for raster format
    packed = np.packbits(bits_inverted, axis=1)
    raster_data = packed.tobytes()

    # ESC/POS header
    width_bytes = (img_bw.width + 7) // 8
    xL = width_bytes & 0xFF
    xH = (width_bytes >> 8) & 0xFF
    yL = img_bw.height & 0xFF
    yH = (img_bw.height >> 8) & 0xFF
    header = b'\x1D\x76\x30\x00' + bytes([xL, xH, yL, yH])

    return header + raster_data

def build_command_stream(image_bytes):
    return (
        b'\x1D\x67\x39'
        b'\x1E\x47\x03'
        b'\x1D\x67\x69'
        b'\x1B\x40'
        b'\x1D\x49\xF0\x19'
        + image_bytes +
        b'\n\n\n\x1D\x56\x00'
    )

def main():
    if len(sys.argv) < 3:
        print("Usage: print_image_final_clean_mask.py <image.png> <B1:2E:43:42:91:48> [--dither]")
        sys.exit(1)

    image_path = sys.argv[1]
    mac = sys.argv[2]
    dither = "--dither" in sys.argv

    print("Converting image...")
    img_data = convert_image_to_escpos_raster(image_path, dither=dither)
    payload = build_command_stream(img_data)

    print(f"Connecting to {mac}...")
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((mac, 1))
    print("Sending...")
    sock.send(payload)
    sock.close()
    print("Done.")

if __name__ == "__main__":
    main()