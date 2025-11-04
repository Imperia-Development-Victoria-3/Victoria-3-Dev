import os
import re

SOURCE_ID = 1  # Define the source machine ID
FILENAME_PATTERN = re.compile(r"savegame_oos_machineid_(\d+)\.oos")
pattern = re.compile(
    r'(tooltip:dw_[\d\w]+),.*?,')  # Pattern needed to discard irrelevant tooltip hashes (they are different even when players are synced)


def clean_tooltip(line):
    return re.sub(pattern, '', line)

def find_first_common_line(lines1,lines2, index_1, index_2):
    index_1 += 1
    index_2 += 1
    offset = 0

    while (index_1 + offset) < len(lines1) and (index_2 + offset) < len(lines2):
        offset = 0
        for i in range(1000):
            if not ((index_1 + offset) < len(lines1) and (index_2 + offset) < len(lines2)):
                offset = 0
                break
            
            if lines1[index_1 + offset] == lines2[index_2]:
                return index_1 + offset, index_2
            
            if lines1[index_1] == lines2[index_2 + offset]:
                return index_1, index_2 + offset

            offset += 1
        index_1 += 1
        index_2 += 1
    return len(lines1) - 1 , len(lines2) - 1

def compare_files(file1, file2):
    with open(file1, 'r', encoding='latin-1') as f1, open(file2, 'r', encoding='latin-1') as f2:
        # Read lines from both files, clean tooltip parts, and sort them
        lines1 = [clean_tooltip(line.strip()) for line in f1 if line.strip()]
        lines2 = [clean_tooltip(line.strip()) for line in f2 if line.strip()]

        # Get the maximum number of lines to avoid index errors
        max_lines = max(len(lines1), len(lines2))

        # Check if there are any differences
        differences = False
        i_1, i_2 = 0, 0
        while i_1 < max_lines and i_2 < max_lines:
            line1 = lines1[i_1] if i_1 < len(lines1) else "No line in file 1"
            line2 = lines2[i_2] if i_2 < len(lines2) else "No line in file 2"

            if line1 != line2:
                if not differences:
                    print("Differences found:")
                differences = True
                tmp_i_1, tmp_i_2 = i_1, i_2
                i_1, i_2 = find_first_common_line(lines1, lines2, i_1, i_2)

                print(f"Line {tmp_i_1}:{i_1} vs {tmp_i_2}:{i_2} differs:")
                print(f"{file1}: {lines1[tmp_i_1:i_1]}")
                print(f"{file2}: {lines2[tmp_i_2:i_2]}")
            else:
                i_1 += 1
                i_2 += 1

        if not differences:
            print(f"No differences found between {file1} and {file2}. Files are identical in content.")



if __name__ == "__main__":
    folder = "fcccaddfccd46a1f_8_9" # CHANGE FOLDER NAME to relevant location
    files = os.listdir(folder)

    # Find all savegame files
    save_files = [f for f in files if FILENAME_PATTERN.match(f)]

    # Identify source file
    source_filename = f"savegame_oos_machineid_{SOURCE_ID}.oos"
    source_path = os.path.join(folder, source_filename)

    if not os.path.isfile(source_path):
        print(f"Source file {source_filename} not found in {folder}.")
        exit(1)

    # Compare each file to source
    for filename in save_files:
        match = FILENAME_PATTERN.match(filename)
        if match:
            machine_id = int(match.group(1))
            if machine_id == SOURCE_ID:
                continue  # Skip comparison with self

            target_path = os.path.join(folder, filename)
            compare_files(source_path, target_path)
