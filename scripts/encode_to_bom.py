import os
import codecs

def is_utf8_bom(file_path):
    """
    Check if a file is encoded in UTF-8 with BOM
    """
    try:
        with open(file_path, 'rb') as f:
            raw = f.read(4)  # Read first 4 bytes for BOM detection
        return raw.startswith(codecs.BOM_UTF8)
    except IOError:
        print(f"Error opening file: {file_path}")
        return False

def convert_to_utf8_bom(file_path):
    """
    Convert file encoding to UTF-8 with BOM
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
        with open(file_path, 'w', encoding='utf-8-sig') as file:
            file.write(content)
    except IOError:
        print(f"Error processing file: {file_path}")

def process_files(directory):
    """
    Process all txt files in the specified directory
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                if not is_utf8_bom(file_path):
                    print(f"Converting: {file_path}")
                    convert_to_utf8_bom(file_path)
                else:
                    print(f"Already UTF-8 BOM: {file_path}")

# Replace '.' with your directory path
process_files('.')
