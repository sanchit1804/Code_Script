import os
import sys

def get_folder_size(path):
    total_size = 0
    # Walk through all directories and files inside the given path
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # Check if file exists and is not a symbolic link
            if not os.path.islink(fp) and os.path.exists(fp):
                try:
                    total_size += os.path.getsize(fp) # Add file size (in bytes)
                except (PermissionError, FileNotFoundError):
                    pass
    return total_size


def format_size(size_in_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024:
            # Return formatted size when it fits the current unit
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024
    return f"{size_in_bytes:.2f} PB"


def main():
    # Ensure a folder path is provided as command-line argument
    if len(sys.argv) < 2:
        print("Usage: python folder_size_calculator.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1] # Read the folder path from arguments

    if not os.path.exists(folder_path):
        print(f"Error: The path '{folder_path}' does not exist.")
        sys.exit(1)

    print(f"\nCalculating folder sizes inside: {folder_path}\n")

    total_size = 0 # Variable to store total folder size

    # Loop through everything inside the given folder
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            size = get_folder_size(item_path)
            print(f"{item}/".ljust(45) + f"= {format_size(size)}")
            total_size += size

        # If the item is a file — get its direct size
        elif os.path.isfile(item_path):
            try:
                size = os.path.getsize(item_path)
                print(f"{item}".ljust(45) + f"= {format_size(size)}")
                total_size += size
            except (PermissionError, FileNotFoundError):
                pass
            
    # Finally, print total folder size
    print(f"Total size of '{folder_path}': {format_size(total_size)}")

if __name__ == "__main__":
    main()
