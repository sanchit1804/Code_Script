#!/usr/bin/env python3
"""
Quick Example Script for Image Resizer & Compressor
===================================================
This script demonstrates how to use the ImageProcessor class programmatically.
"""

from pathlib import Path
from image_resizer_compressor import ImageProcessor


def example_1_resize_by_width():
    """Example 1: Resize images to 800px width, maintain aspect ratio."""
    print("\n" + "="*60)
    print("Example 1: Resize by width (800px)")
    print("="*60)
    
    processor = ImageProcessor(
        input_dir="./sample_images",
        output_dir="./output/example1_width_800"
    )
    
    processor.batch_process(
        method="pillow",
        width=800,
        quality=85,
        maintain_aspect=True
    )


def example_2_resize_by_percentage():
    """Example 2: Resize images to 50% of original size."""
    print("\n" + "="*60)
    print("Example 2: Resize by percentage (50%)")
    print("="*60)
    
    processor = ImageProcessor(
        input_dir="./sample_images",
        output_dir="./output/example2_50_percent"
    )
    
    processor.batch_process(
        method="pillow",
        scale_percent=50,
        quality=90
    )


def example_3_compress_only():
    """Example 3: Compress images without resizing."""
    print("\n" + "="*60)
    print("Example 3: Compress only (no resize)")
    print("="*60)
    
    processor = ImageProcessor(
        input_dir="./sample_images",
        output_dir="./output/example3_compress_only"
    )
    
    processor.batch_process(
        method="pillow",
        quality=80
    )


def example_4_specific_dimensions():
    """Example 4: Resize to specific dimensions (1024x768)."""
    print("\n" + "="*60)
    print("Example 4: Resize to 1024x768")
    print("="*60)
    
    processor = ImageProcessor(
        input_dir="./sample_images",
        output_dir="./output/example4_1024x768"
    )
    
    processor.batch_process(
        method="pillow",
        width=1024,
        height=768,
        quality=85,
        maintain_aspect=False
    )


def example_5_opencv_method():
    """Example 5: Use OpenCV for processing."""
    print("\n" + "="*60)
    print("Example 5: OpenCV method (resize by height)")
    print("="*60)
    
    processor = ImageProcessor(
        input_dir="./sample_images",
        output_dir="./output/example5_opencv"
    )
    
    processor.batch_process(
        method="opencv",
        height=600,
        quality=85
    )


def example_6_thumbnail_creation():
    """Example 6: Create small thumbnails."""
    print("\n" + "="*60)
    print("Example 6: Create thumbnails (25% size)")
    print("="*60)
    
    processor = ImageProcessor(
        input_dir="./sample_images",
        output_dir="./output/example6_thumbnails"
    )
    
    processor.batch_process(
        method="pillow",
        scale_percent=25,
        quality=80
    )


def main():
    """Run all examples."""
    print("""
╔══════════════════════════════════════════════════════════╗
║        Image Resizer & Compressor - Examples            ║
║              Programmatic Usage Demos                    ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    print("This script will run 6 different examples.")
    print("Make sure you have sample images in ./sample_images/")
    print()
    
    input("Press Enter to start...")
    
    # Run all examples
    try:
        example_1_resize_by_width()
        example_2_resize_by_percentage()
        example_3_compress_only()
        example_4_specific_dimensions()
        example_5_opencv_method()
        example_6_thumbnail_creation()
        
        print("\n" + "="*60)
        print("✓ All examples completed successfully!")
        print("Check the ./output/ directory for results")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error running examples: {str(e)}")
        print("Make sure you have sample images in ./sample_images/")


if __name__ == "__main__":
    main()
