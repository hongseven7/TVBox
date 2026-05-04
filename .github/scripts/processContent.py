import re
import sys
import os
import glob
import hashlib

def calculateMd5(file_path):
    if not os.path.isfile(file_path):
        return None 
    try:    
        with open(file_path, "rb") as f:
            file_hash = hashlib.md5()
            while chunk := f.read(8192):
                file_hash.update(chunk)
        return file_hash.hexdigest()
    except:
        return None

def callbackMd5(match):
    # Group 1: The leading slash '/'
    slash = match.group(1)
    
    # Group 2: The filename (no slashes)
    filename = match.group(2)
    
    # Group 3: The old checksum
    old_checksum = match.group(3)
    
    # Calculate NEW checksum
    new_checksum = calculateMd5(filename)
    
    if new_checksum and (new_checksum != old_checksum):
        print(f"Updated: {filename} ({old_checksum} -> {new_checksum})")
        # Reconstruct the string: Slash + Filename + ;md5; + NewHash + closing Quote
        return f"{slash}{filename};md5;{new_checksum}\""
    else:
        # Return original match if file not found
        return match.group(0)

def processContent(input_file_path, output_file_path):
    # https://                  -> Literal start
    # [^"'\s]* -> Match 0+ chars that are NOT quotes or whitespace
    # raw\.githubusercontent... -> Your specific target ending with user name
    pattern_proxy = r"https://[^\"'\s]*raw\.githubusercontent\.com"
    replacement_proxy = r"https://raw.githubusercontent.com"
    
    pattern_username = r"yoursmile66"
    replacement_username = r"hongseven7"
    
    pattern_jar_url = r"jihulab.com/yoursmile3/TVBox/-/raw/main"
    replacement_jar_url = r"raw.githubusercontent.com/hongseven7/TVBox/main"
    
    # (/):        Group 1 - Match the literal leading slash
    # ([^/]+):    Group 2 - Match filename (1+ chars that are NOT a slash)
    # ;md5;:      Match the literal separator
    # ([a-f0-9]+):Group 3 - Match the hex checksum
    # ":          Match the closing quote (consumed by regex, so we must put it back)
    pattern_md5 = r'(/)([^/]+);md5;([a-fA-F0-9]+)"'
    
    total_changes = 0

    # Read the file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Perform the replacements
    content, changes = re.subn(pattern_proxy, replacement_proxy, content)
    print(f"Changed {changes} lines with proxy.")
    total_changes += changes
    content, changes = re.subn(pattern_username, replacement_username, content)
    print(f"Changed {changes} lines with user name.")
    total_changes += changes
    content, changes = re.subn(pattern_jar_url, replacement_jar_url, content)
    print(f"Changed {changes} lines with jar URL.")
    total_changes += changes
    content, changes = re.subn(pattern_md5, callbackMd5, content)
    print(f"Changed {changes} lines with MD5 checksum.")
    total_changes += changes

    if total_changes == 0:
        return

    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(content)

    print(f"Success! Processed content saved to {output_file_path} with {total_changes} changes.")

def main():
    # The file extension to target
    file_pattern = '*.json'

    if len(sys.argv) < 2:
        print("Command-line arguments for directory name not found")
        sys.exit()

    input_dir = sys.argv[1]

    # Construct path: ./input_dir/**/*.txt
    # The '**' tells glob to match directories recursively
    search_path = os.path.join(input_dir, '**', file_pattern)

    # recursive=True is required to make the '**' pattern work
    files = glob.glob(search_path, recursive=True)

    if not files:
        print(f"No files matching '{file_pattern}' found in '{input_dir}' or its subdirectories.")
        return

    print(f"Found {len(files)} files in total. Start processing...\n")

    for file in files:
        processContent(file, file)

    print("\nProcessing complete.")

if __name__ == "__main__":
    main()
