#!/usr/bin/env python3
"""
Image Resizer and Compressor
============================
A script to resize and compress images in bulk to reduce file sizes.
Supports multiple image formats: JPG, PNG, JPEG, BMP, WEBP, TIFF

Features:
- Resize images by width, height, or percentage
- Compress images with quality control
- Batch processing of multiple images
- Support for both Pillow and OpenCV
- Maintains aspect ratio option
- Creates output directory automatically

Author: Hacktoberfest 2025 Contributor
"""

import os
import sys
from pathlib import Path
from PIL import Image
import cv2
import numpy as np
from typing import Tuple, List, Optional


class ImageProcessor:
    """Class to handle image resizing and compression operations."""
    
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff', '.tif'}
    
    def __init__(self, input_dir: str, output_dir: str = None):
        """
        Initialize the ImageProcessor.
        
        Args:
            input_dir: Directory containing input images
            output_dir: Directory for output images (default: input_dir/compressed)
        """
        self.input_dir = Path(input_dir)
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            self.output_dir = self.input_dir / "compressed"
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def get_image_files(self) -> List[Path]:
        """Get all supported image files from input directory."""
        image_files = []
        for file_path in self.input_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in self.SUPPORTED_FORMATS:
                image_files.append(file_path)
        return image_files
    
    def resize_with_pillow(
        self,
        image_path: Path,
        output_path: Path,
        width: Optional[int] = None,
        height: Optional[int] = None,
        scale_percent: Optional[int] = None,
        quality: int = 85,
        maintain_aspect: bool = True
    ) -> bool:
        """
        Resize and compress image using Pillow.
        
        Args:
            image_path: Path to input image
            output_path: Path to save output image
            width: Target width in pixels
            height: Target height in pixels
            scale_percent: Scale percentage (e.g., 50 for 50%)
            quality: Compression quality (1-100, higher is better)
            maintain_aspect: Whether to maintain aspect ratio
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with Image.open(image_path) as img:
                original_size = img.size
                
                # Calculate new dimensions
                if scale_percent:
                    new_width = int(img.width * scale_percent / 100)
                    new_height = int(img.height * scale_percent / 100)
                elif width and height:
                    new_width = width
                    new_height = height
                elif width:
                    new_width = width
                    new_height = int(img.height * (width / img.width)) if maintain_aspect else img.height
                elif height:
                    new_height = height
                    new_width = int(img.width * (height / img.height)) if maintain_aspect else img.width
                else:
                    new_width, new_height = img.size
                
                # Resize image
                resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Save with compression
                if image_path.suffix.lower() in ['.jpg', '.jpeg']:
                    resized_img.save(output_path, 'JPEG', quality=quality, optimize=True)
                elif image_path.suffix.lower() == '.png':
                    resized_img.save(output_path, 'PNG', optimize=True, compress_level=9)
                else:
                    resized_img.save(output_path, quality=quality, optimize=True)
                
                # Calculate size reduction
                original_size_kb = image_path.stat().st_size / 1024
                compressed_size_kb = output_path.stat().st_size / 1024
                reduction = ((original_size_kb - compressed_size_kb) / original_size_kb) * 100
                
                print(f"✓ {image_path.name}")
                print(f"  Original: {original_size} ({original_size_kb:.2f} KB)")
                print(f"  New: {new_width}x{new_height} ({compressed_size_kb:.2f} KB)")
                print(f"  Size reduction: {reduction:.2f}%\n")
                
                return True
        except Exception as e:
            print(f"✗ Error processing {image_path.name}: {str(e)}\n")
            return False
    
    def resize_with_opencv(
        self,
        image_path: Path,
        output_path: Path,
        width: Optional[int] = None,
        height: Optional[int] = None,
        scale_percent: Optional[int] = None,
        quality: int = 85
    ) -> bool:
        """
        Resize and compress image using OpenCV.
        
        Args:
            image_path: Path to input image
            output_path: Path to save output image
            width: Target width in pixels
            height: Target height in pixels
            scale_percent: Scale percentage (e.g., 50 for 50%)
            quality: Compression quality (1-100, higher is better)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Read image
            img = cv2.imread(str(image_path))
            if img is None:
                raise ValueError(f"Could not read image: {image_path}")
            
            original_height, original_width = img.shape[:2]
            original_size = (original_width, original_height)
            
            # Calculate new dimensions
            if scale_percent:
                new_width = int(original_width * scale_percent / 100)
                new_height = int(original_height * scale_percent / 100)
            elif width and height:
                new_width = width
                new_height = height
            elif width:
                aspect_ratio = original_height / original_width
                new_width = width
                new_height = int(width * aspect_ratio)
            elif height:
                aspect_ratio = original_width / original_height
                new_height = height
                new_width = int(height * aspect_ratio)
            else:
                new_width, new_height = original_width, original_height
            
            # Resize image
            resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
            
            # Save with compression
            if image_path.suffix.lower() in ['.jpg', '.jpeg']:
                cv2.imwrite(str(output_path), resized_img, [cv2.IMWRITE_JPEG_QUALITY, quality])
            elif image_path.suffix.lower() == '.png':
                compression = int((100 - quality) / 10)  # Convert to PNG compression level (0-9)
                cv2.imwrite(str(output_path), resized_img, [cv2.IMWRITE_PNG_COMPRESSION, compression])
            else:
                cv2.imwrite(str(output_path), resized_img)
            
            # Calculate size reduction
            original_size_kb = image_path.stat().st_size / 1024
            compressed_size_kb = output_path.stat().st_size / 1024
            reduction = ((original_size_kb - compressed_size_kb) / original_size_kb) * 100
            
            print(f"✓ {image_path.name}")
            print(f"  Original: {original_size} ({original_size_kb:.2f} KB)")
            print(f"  New: {new_width}x{new_height} ({compressed_size_kb:.2f} KB)")
            print(f"  Size reduction: {reduction:.2f}%\n")
            
            return True
        except Exception as e:
            print(f"✗ Error processing {image_path.name}: {str(e)}\n")
            return False
    
    def batch_process(
        self,
        method: str = "pillow",
        width: Optional[int] = None,
        height: Optional[int] = None,
        scale_percent: Optional[int] = None,
        quality: int = 85,
        maintain_aspect: bool = True
    ) -> Tuple[int, int]:
        """
        Process all images in the input directory.
        
        Args:
            method: Processing method ('pillow' or 'opencv')
            width: Target width in pixels
            height: Target height in pixels
            scale_percent: Scale percentage
            quality: Compression quality (1-100)
            maintain_aspect: Whether to maintain aspect ratio (Pillow only)
        
        Returns:
            Tuple of (successful_count, failed_count)
        """
        image_files = self.get_image_files()
        
        if not image_files:
            print(f"No supported image files found in {self.input_dir}")
            return 0, 0
        
        print(f"\nFound {len(image_files)} image(s) to process")
        print(f"Output directory: {self.output_dir}\n")
        print("=" * 60)
        
        successful = 0
        failed = 0
        
        for image_path in image_files:
            output_path = self.output_dir / image_path.name
            
            if method.lower() == "opencv":
                success = self.resize_with_opencv(
                    image_path, output_path, width, height, scale_percent, quality
                )
            else:  # Default to Pillow
                success = self.resize_with_pillow(
                    image_path, output_path, width, height, scale_percent, quality, maintain_aspect
                )
            
            if success:
                successful += 1
            else:
                failed += 1
        
        print("=" * 60)
        print(f"\nProcessing complete!")
        print(f"✓ Successful: {successful}")
        print(f"✗ Failed: {failed}")
        print(f"\nProcessed images saved to: {self.output_dir}")
        
        return successful, failed


def main():
    """Main function to run the image processor."""
    print("""
╔══════════════════════════════════════════════════════════╗
║     Image Resizer & Compressor - Bulk Processing        ║
║              Hacktoberfest 2025 Project                  ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # Get user input
    input_dir = input("Enter input directory path: ").strip()
    
    if not input_dir or not os.path.isdir(input_dir):
        print("❌ Invalid directory path!")
        sys.exit(1)
    
    output_dir = input("Enter output directory path (press Enter for default): ").strip()
    if not output_dir:
        output_dir = None
    
    # Choose processing method
    print("\nChoose processing method:")
    print("1. Pillow (recommended for general use)")
    print("2. OpenCV (for advanced processing)")
    method_choice = input("Enter choice (1 or 2): ").strip()
    method = "opencv" if method_choice == "2" else "pillow"
    
    # Choose resize option
    print("\nChoose resize option:")
    print("1. Resize by width (maintain aspect ratio)")
    print("2. Resize by height (maintain aspect ratio)")
    print("3. Resize by percentage")
    print("4. Resize by specific width and height")
    print("5. Compress only (no resize)")
    
    resize_choice = input("Enter choice (1-5): ").strip()
    
    width = None
    height = None
    scale_percent = None
    maintain_aspect = True
    
    try:
        if resize_choice == "1":
            width = int(input("Enter target width in pixels: "))
        elif resize_choice == "2":
            height = int(input("Enter target height in pixels: "))
        elif resize_choice == "3":
            scale_percent = int(input("Enter scale percentage (e.g., 50 for 50%): "))
        elif resize_choice == "4":
            width = int(input("Enter target width in pixels: "))
            height = int(input("Enter target height in pixels: "))
            maintain_aspect = False
        elif resize_choice == "5":
            pass  # No resize, only compress
        else:
            print("Invalid choice, using default (compress only)")
    except ValueError:
        print("Invalid input, using default values")
    
    # Get quality setting
    try:
        quality = int(input("\nEnter compression quality (1-100, recommended 85): ").strip() or "85")
        quality = max(1, min(100, quality))  # Clamp between 1 and 100
    except ValueError:
        quality = 85
    
    # Process images
    processor = ImageProcessor(input_dir, output_dir)
    processor.batch_process(
        method=method,
        width=width,
        height=height,
        scale_percent=scale_percent,
        quality=quality,
        maintain_aspect=maintain_aspect
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Process interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        sys.exit(1)
