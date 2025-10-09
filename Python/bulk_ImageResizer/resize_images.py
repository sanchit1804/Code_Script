# resize_images.py

import os
import argparse
from PIL import Image

def resize_images(input_folder, output_folder, size):
    """
    Resizes all JPG, PNG, and WebP images in a folder to a specified size.

    Args:
        input_folder (str): The path to the folder containing images.
        output_folder (str): The path to the folder to save resized images.
        size (tuple): A tuple of (width, height) for the target resolution.
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created directory: {output_folder}")

    # List all files in the input directory
    files = os.listdir(input_folder)

    for filename in files:
        # Check for valid image extensions (case-insensitive) - NOW INCLUDES .webp
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            try:
                # Construct full file paths
                input_path = os.path.join(input_folder, filename)
                output_path = os.path.join(output_folder, filename)

                # Open, resize, and save the image
                with Image.open(input_path) as img:
                    # Convert to RGB to avoid issues when saving formats like JPG
                    # from formats that might have transparency (like PNG or WebP).
                    rgb_img = img.convert('RGB')
                    resized_img = rgb_img.resize(size)
                    resized_img.save(output_path)
                    print(f"Successfully resized {filename}")

            except Exception as e:
                print(f"Error processing {filename}: {e}")
    
    print("\nBatch resize complete! ✨")

if __name__ == "__main__":
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Batch resize images in a folder.")
    
    # Required positional arguments
    parser.add_argument("input_folder", type=str, help="Path to the input folder containing images.")
    parser.add_argument("output_folder", type=str, help="Path to the folder to save resized images.")
    
    # Required optional argument for size
    parser.add_argument("--size", type=int, nargs=2, required=True, metavar=('WIDTH', 'HEIGHT'), 
                        help="Target size for resizing (e.g., --size 800 600).")

    args = parser.parse_args()

    # Convert the size list to a tuple
    target_size = tuple(args.size)
    
    # Run the main function
    resize_images(args.input_folder, args.output_folder, target_size)