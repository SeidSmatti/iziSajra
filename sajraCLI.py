#!/usr/bin/env python3
import os
import sys
import argparse

def get_directory_tree(directory, include_hidden, level=0):
    tree_str = ""
    indent = "  " * level
    tree_str += "{}{}/\n".format(indent, os.path.basename(directory))
    try:
        for item in os.listdir(directory):
            if not include_hidden and item.startswith('.'):
                continue  # Skip hidden files and directories
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                tree_str += get_directory_tree(item_path, include_hidden, level + 1)
            else:
                tree_str += "{}  {}\n".format(indent, item)
    except OSError:
        # Covers permission errors and other OS-related errors
        tree_str += "{}  [Permission Denied]\n".format(indent)
    return tree_str

def extract_directory_data(directory, include_hidden):
    output_text = "DIRECTORY STRUCTURE :\n{}\n\n".format(directory)
    output_text += get_directory_tree(directory, include_hidden)
    output_text += "\nFILES:\n____\n"

    for root, dirs, files in os.walk(directory):
        if not include_hidden:
            # Modify dirs in-place to skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            # Filter out hidden files
            files = [f for f in files if not f.startswith('.')]
        for filename in files:
            if not include_hidden and filename.startswith('.'):
                continue  # Skip hidden files
            file_path = os.path.join(root, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_content = file.read()
                    output_text += "{}:\n\n{}\n____\n".format(filename, file_content)
            except (UnicodeDecodeError, IOError, OSError):
                # Covers binary files, permission issues, directories (if encountered as files), etc.
                output_text += "{}:\n\n[Cannot read file content]\n____\n".format(filename)
    return output_text

def main():
    parser = argparse.ArgumentParser(description='Directory Extractor')
    parser.add_argument('directory', nargs='?', default='.', help='Directory to extract (default: current directory)')
    parser.add_argument('-i', '--include-hidden', action='store_true', help='Include hidden files and directories')
    parser.add_argument('-o', '--output', help='Output file to save the extracted data')
    args = parser.parse_args()

    directory = args.directory
    include_hidden = args.include_hidden
    output_file = args.output

    if not os.path.isdir(directory):
        print("Error: {} is not a valid directory".format(directory))
        sys.exit(1)

    output_text = extract_directory_data(directory, include_hidden)

    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output_text)
            print("Output saved to {}".format(output_file))
        except Exception as e:
            print("Error: Failed to save output to {}: {}".format(output_file, e))
    else:
        print(output_text)

if __name__ == '__main__':
    main()

