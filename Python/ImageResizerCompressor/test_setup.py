#!/usr/bin/env python3
"""
Test Script for Image Resizer & Compressor
===========================================
This script verifies that all dependencies are installed correctly
and creates a test image to verify the functionality.
"""

import sys
from pathlib import Path


def test_imports():
    """Test if all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import PIL
        from PIL import Image
        print("✓ Pillow installed:", PIL.__version__)
    except ImportError as e:
        print("✗ Pillow not installed:", str(e))
        return False
    
    try:
        import cv2
        print("✓ OpenCV installed:", cv2.__version__)
    except ImportError as e:
        print("✗ OpenCV not installed:", str(e))
        return False
    
    try:
        import numpy as np
        print("✓ NumPy installed:", np.__version__)
    except ImportError as e:
        print("✗ NumPy not installed:", str(e))
        return False
    
    return True


def create_test_image():
    """Create a test image for demonstration."""
    print("\nCreating test image...")
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        import numpy as np
        
        # Create a colorful test image
        width, height = 1200, 800
        
        # Create gradient background
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
        # Draw gradient
        for y in range(height):
            r = int(255 * (y / height))
            g = int(255 * (1 - y / height))
            b = 128
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Draw some shapes
        draw.rectangle([100, 100, 300, 300], outline='white', width=5)
        draw.ellipse([400, 150, 700, 450], fill='yellow', outline='orange', width=5)
        draw.polygon([(900, 200), (1000, 400), (800, 400)], fill='cyan', outline='blue', width=5)
        
        # Add text
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
        except:
            font = ImageFont.load_default()
        
        draw.text((width//2 - 200, height//2 - 50), "TEST IMAGE", fill='white', font=font)
        draw.text((width//2 - 220, height//2 + 30), "1200 x 800", fill='white', font=font)
        
        # Save test images
        sample_dir = Path("./sample_images")
        sample_dir.mkdir(exist_ok=True)
        
        # Save as different formats
        img.save(sample_dir / "test_image_1.jpg", quality=95)
        img.save(sample_dir / "test_image_2.png")
        
        # Create a second test image (different size)
        img2 = img.resize((800, 600))
        img2.save(sample_dir / "test_image_3.jpg", quality=95)
        
        print(f"✓ Created 3 test images in {sample_dir}")
        print(f"  - test_image_1.jpg (1200x800)")
        print(f"  - test_image_2.png (1200x800)")
        print(f"  - test_image_3.jpg (800x600)")
        
        return True
        
    except Exception as e:
        print(f"✗ Failed to create test image: {str(e)}")
        return False


def test_script_import():
    """Test if the main script can be imported."""
    print("\nTesting main script...")
    
    try:
        from image_resizer_compressor import ImageProcessor
        print("✓ ImageProcessor class loaded successfully")
        return True
    except ImportError as e:
        print(f"✗ Failed to import main script: {str(e)}")
        return False
    except Exception as e:
        print(f"✗ Error loading script: {str(e)}")
        return False


def run_quick_test():
    """Run a quick functionality test."""
    print("\nRunning quick functionality test...")
    
    try:
        from image_resizer_compressor import ImageProcessor
        from pathlib import Path
        
        # Check if test images exist
        sample_dir = Path("./sample_images")
        test_images = list(sample_dir.glob("test_image_*.jpg")) + list(sample_dir.glob("test_image_*.png"))
        
        if not test_images:
            print("⚠ No test images found. Run this script again to create them.")
            return True
        
        print(f"Found {len(test_images)} test image(s)")
        
        # Test basic processing
        processor = ImageProcessor(
            input_dir="./sample_images",
            output_dir="./sample_images/test_output"
        )
        
        # Process with 50% scale
        successful, failed = processor.batch_process(
            method="pillow",
            scale_percent=50,
            quality=85
        )
        
        if successful > 0:
            print(f"\n✓ Successfully processed {successful} image(s)")
            print(f"  Check ./sample_images/test_output/ for results")
            return True
        else:
            print(f"\n⚠ No images were processed")
            return False
            
    except Exception as e:
        print(f"✗ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("""
╔══════════════════════════════════════════════════════════╗
║     Image Resizer & Compressor - Test Script           ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    all_passed = True
    
    # Test 1: Imports
    print("\n[Test 1/4] Checking dependencies...")
    if not test_imports():
        print("\n❌ Please install dependencies:")
        print("   pip install -r requirements.txt")
        all_passed = False
    
    # Test 2: Script import
    print("\n[Test 2/4] Checking main script...")
    if not test_script_import():
        all_passed = False
    
    # Test 3: Create test images
    if all_passed:
        print("\n[Test 3/4] Creating test images...")
        if not create_test_image():
            all_passed = False
    
    # Test 4: Run functionality test
    if all_passed:
        print("\n[Test 4/4] Testing image processing...")
        if not run_quick_test():
            all_passed = False
    
    # Final result
    print("\n" + "="*60)
    if all_passed:
        print("✅ All tests passed! The script is ready to use.")
        print("\nNext steps:")
        print("1. Add your own images to ./sample_images/")
        print("2. Run: python image_resizer_compressor.py")
        print("3. Or try: python example_usage.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
    print("="*60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠ Tests interrupted by user.")
        sys.exit(1)
