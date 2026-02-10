import re
import sys
import os
import glob

def processContent(input_file_path, output_file_path):
    # Regex explanation:
    # https://                  -> Literal start
    # [^"'\s]* -> Match 0+ chars that are NOT quotes or whitespace
    # raw\.githubusercontent... -> Your specific target ending with user name
    pattern_proxy = r"https://[^\"'\s]*raw\.githubusercontent\.com/yoursmile66"
    replacement_proxy = r"https://raw.githubusercontent.com/hongseven7"
    
    pattern_jar_url = r"jihulab.com/yoursmile2/TVBox/-/raw/master"
    replacement_jar_url = r"raw.githubusercontent.com/hongseven7/TVBox/main"
    
    total_changes = 0

    # Read the file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Perform the replacements
    content, changes = re.subn(pattern_proxy, replacement_proxy, content)
    total_changes += changes
    content, changes = re.subn(pattern_jar_url, replacement_jar_url, content)
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
