#!/usr/bin/env python3
"""
Quick Test Script - Pillow Only Version
Tests the image processor with just Pillow (no OpenCV required)
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from PIL import Image
    print("✓ Pillow is installed and working!")
    print(f"  Version: {Image.__version__ if hasattr(Image, '__version__') else 'Unknown'}")
except ImportError as e:
    print(f"✗ Pillow not installed: {e}")
    sys.exit(1)

# Check for images in ingest folder
ingest_dir = Path("./ingest")
image_files = list(ingest_dir.glob("*.png")) + list(ingest_dir.glob("*.jpg")) + list(ingest_dir.glob("*.jpeg"))

if not image_files:
    print("\n⚠ No images found in ingest folder")
    sys.exit(1)

print(f"\n✓ Found {len(image_files)} image(s) in ingest folder")
for i, img in enumerate(image_files[:5], 1):
    size_kb = img.stat().st_size / 1024
    print(f"  {i}. {img.name} ({size_kb:.1f} KB)")
if len(image_files) > 5:
    print(f"  ... and {len(image_files) - 5} more")

# Test processing one image
print("\n🧪 Testing image processing...")
test_image = image_files[0]
output_dir = Path("./output")
output_dir.mkdir(exist_ok=True)

try:
    # Open and resize
    with Image.open(test_image) as img:
        original_size = img.size
        original_kb = test_image.stat().st_size / 1024
        
        # Resize to 800px width
        new_width = 800
        aspect_ratio = img.height / img.width
        new_height = int(new_width * aspect_ratio)
        
        resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Save
        output_path = output_dir / test_image.name
        if test_image.suffix.lower() in ['.jpg', '.jpeg']:
            resized.save(output_path, 'JPEG', quality=85, optimize=True)
        elif test_image.suffix.lower() == '.png':
            resized.save(output_path, 'PNG', optimize=True, compress_level=9)
        else:
            resized.save(output_path, quality=85, optimize=True)
        
        output_kb = output_path.stat().st_size / 1024
        reduction = ((original_kb - output_kb) / original_kb) * 100
        
        print(f"\n✓ Successfully processed test image!")
        print(f"  Original: {original_size[0]}x{original_size[1]} ({original_kb:.1f} KB)")
        print(f"  Resized:  {new_width}x{new_height} ({output_kb:.1f} KB)")
        print(f"  Reduction: {reduction:.1f}%")
        print(f"  Saved to: {output_path}")
        
except Exception as e:
    print(f"\n✗ Error processing image: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*60)
print("✅ TEST PASSED! Everything is working!")
print("="*60)
print("\nYou can now process all images with:")
print("  python3 cli_interface_pillow.py")
print("\nOr use the web preset:")
print("  python3 cli_interface_pillow.py --config web")
