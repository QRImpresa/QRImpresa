import qrcode
from PIL import Image

def generate_qr(url: str, out_path: str = "qr.png", size: int = 1024):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    img = img.resize((size, size))
    img.save(out_path)
    print(f"QR generato: {out_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python generate_qr.py <url> [out_path]")
    else:
        url = sys.argv[1]
        out = sys.argv[2] if len(sys.argv) > 2 else "qr.png"
        generate_qr(url, out)
