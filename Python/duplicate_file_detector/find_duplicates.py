import os
import hashlib
from collections import defaultdict

def get_file_hash(path, chunk_size=8192):
    """Generate SHA256 hash for a file."""
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            while chunk := f.read(chunk_size):
                h.update(chunk)
        return h.hexdigest()
    except (PermissionError, FileNotFoundError):
        return None

def scan_folder(folder_path, mode="hash"):
    """Scan folder and find duplicates based on mode ('name', 'size', or 'hash')."""
    duplicates = defaultdict(list)
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if mode == "name":
                key = file
            elif mode == "size":
                try:
                    key = os.path.getsize(file_path)
                except OSError:
                    continue
            elif mode == "hash":
                key = get_file_hash(file_path)
                if not key:
                    continue
            else:
                raise ValueError("Mode must be 'name', 'size', or 'hash'.")
            duplicates[key].append(file_path)
    return {k: v for k, v in duplicates.items() if len(v) > 1}

def display_duplicates(duplicates):
    if not duplicates:
        print("✅ No duplicates found.")
        return
    print("\n🔍 Duplicate Files Found:\n")
    for group, files in duplicates.items():
        print(f"Group ({len(files)} files):")
        for f in files:
            print("  ", f)
        print("-" * 60)

def delete_duplicates(duplicates):
    for group, files in duplicates.items():
        keep = files[0]
        print(f"\nKeeping: {keep}")
        for f in files[1:]:
            try:
                os.remove(f)
                print(f"🗑 Deleted duplicate: {f}")
            except Exception as e:
                print(f"⚠️ Could not delete {f}: {e}")

if __name__ == "__main__":
    folder = input("Enter folder path to scan: ").strip()
    print("\nSelect comparison mode:")
    print("1. By name\n2. By size\n3. By hash (recommended)")
    mode_choice = input("Enter choice (1/2/3): ").strip()
    mode = {"1": "name", "2": "size", "3": "hash"}.get(mode_choice, "hash")

    duplicates = scan_folder(folder, mode)
    display_duplicates(duplicates)

    if duplicates:
        action = input("\nDo you want to delete duplicates? (y/n): ").strip().lower()
        if action == "y":
            delete_duplicates(duplicates)
            print("\n✅ Deletion complete.")
        else:
            print("\nNo files were deleted.")
