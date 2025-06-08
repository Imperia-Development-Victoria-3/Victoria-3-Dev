import os
import subprocess
from PIL import Image

def is_multiple_of_4(x):
    return x % 4 == 0

def nearest_multiple_of_4(x):
    return max(4, round(x / 4) * 4)

def get_image_size(path):
    try:
        with Image.open(path) as img:
            return img.size
    except Exception as e:
        print(f"❌ Error reading {path}: {e}")
        return None

def is_compressed_dds(file_path):
    try:
        with open(file_path, 'rb') as f:
            f.seek(84)  # DDS header offset for pixel format flags
            flags = f.read(4).decode("utf-8")
            return not (flags == b"DXT5")  # 0x40 means uncompressed RGB
    except Exception as e:
        print(f"❌ Error checking compression for {file_path}: {e}")
        return True  # Assume compressed to avoid unnecessary conversion

def process_dds(file_path, output_dir):
    size = get_image_size(file_path)
    if size is None:
        return

    width, height = size
    needs_resize = not (is_multiple_of_4(width) and is_multiple_of_4(height))
    needs_compression = not is_compressed_dds(file_path)

    if not needs_resize and not needs_compression:
        print(f"✅ {file_path} - OK")
        return

    new_width = nearest_multiple_of_4(width)
    new_height = nearest_multiple_of_4(height)

    command = [
        "./scripts/software/texconv.exe",  # full path if not in PATH
        "-nologo",
        # "-pow2",  # ensure power-of-2 dimensions (optional)
        "-w", f"{new_width}",
        "-h", f"{new_height}",
        "-o", output_dir,
        "-m", "0",
        "-y",  # overwrite
        "-f", "BC3_UNORM",
        file_path
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ texconv failed for {file_path}: {e}")


def scan_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".dds"):
                full_path = os.path.join(root, file)
                process_dds(full_path, root)

if __name__ == "__main__":
    folder = "gfx"
    if not os.path.isdir(folder):
        print("Invalid directory.")
    else:
        scan_folder(folder)
