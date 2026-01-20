import re
import sys
import os
import glob

def remove_proxy(input_file_path, output_file_path):
    # Define the pattern
    # r'(")[^"]*raw\.githubusercontent' explanation:
    # (") -> Capture the opening quote (Group 1)
    # [^"]* -> Match any character that is NOT a quote (ensures we stay inside the current string)
    # raw\.githubusercontent -> The anchor text we are looking for
    pattern = r'(")[^"]*raw\.githubusercontent'

    # Read the file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Perform the replacement
    # We replace the whole match with:
    # \1 -> The original quote captured in Group 1
    # https:// -> The new protocol
    # raw.githubusercontent -> The rest of the required string
    new_content = re.sub(pattern, r'\1https://raw.githubusercontent', content)

    if (content == new_content):
        return

    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)

    print(f"Success! Processed content saved to {output_file_path}")

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
        remove_proxy(file, file)

    print("\nProcessing complete.")

if __name__ == "__main__":
    main()
