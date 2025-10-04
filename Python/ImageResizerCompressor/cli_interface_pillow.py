#!/usr/bin/env python3
"""
Image Resizer & Compressor - Pillow Only Version
================================================
Simplified version using only Pillow (no OpenCV required)

All features work except the OpenCV processing method option.
Perfect for systems where OpenCV is not installed.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List, Tuple
from PIL import Image


class ImageProcessor:
    """Class to handle image resizing and compression operations using Pillow."""
    
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff', '.tif'}
    
    def __init__(self, input_dir: str, output_dir: str = None):
        """Initialize the ImageProcessor."""
        self.input_dir = Path(input_dir)
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            self.output_dir = self.input_dir / "compressed"
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def get_image_files(self) -> List[Path]:
        """Get all supported image files from input directory."""
        image_files = []
        for file_path in self.input_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in self.SUPPORTED_FORMATS:
                image_files.append(file_path)
        return image_files
    
    def resize_and_compress(
        self,
        image_path: Path,
        output_path: Path,
        width: Optional[int] = None,
        height: Optional[int] = None,
        scale_percent: Optional[int] = None,
        quality: int = 85,
        maintain_aspect: bool = True
    ) -> bool:
        """Resize and compress image using Pillow."""
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
                print(f"  Original: {original_size[0]}x{original_size[1]} ({original_size_kb:.2f} KB)")
                print(f"  New: {new_width}x{new_height} ({compressed_size_kb:.2f} KB)")
                print(f"  Size reduction: {reduction:.2f}%\n")
                
                return True
        except Exception as e:
            print(f"✗ Error processing {image_path.name}: {str(e)}\n")
            return False
    
    def batch_process(
        self,
        width: Optional[int] = None,
        height: Optional[int] = None,
        scale_percent: Optional[int] = None,
        quality: int = 85,
        maintain_aspect: bool = True
    ) -> Tuple[int, int]:
        """Process all images in the input directory."""
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
            
            success = self.resize_and_compress(
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


class ConfigManager:
    """Manages configuration presets and user settings."""
    
    CONFIG_FILE = "config.json"
    
    PRESETS = {
        "web": {
            "name": "Web Optimization",
            "width": 1920,
            "height": None,
            "scale_percent": None,
            "quality": 85,
            "maintain_aspect": True,
            "description": "Optimized for web pages (1920px width, 85% quality)"
        },
        "social": {
            "name": "Social Media",
            "width": 1080,
            "height": 1080,
            "scale_percent": None,
            "quality": 90,
            "maintain_aspect": False,
            "description": "Square format for Instagram/Facebook (1080x1080)"
        },
        "email": {
            "name": "Email Attachments",
            "width": None,
            "height": None,
            "scale_percent": 40,
            "quality": 80,
            "maintain_aspect": True,
            "description": "Compressed for email (40% of original, 80% quality)"
        },
        "thumbnail": {
            "name": "Thumbnails",
            "width": 200,
            "height": None,
            "scale_percent": None,
            "quality": 75,
            "maintain_aspect": True,
            "description": "Small thumbnails (200px width, 75% quality)"
        },
        "high_quality": {
            "name": "High Quality",
            "width": 2560,
            "height": None,
            "scale_percent": None,
            "quality": 95,
            "maintain_aspect": True,
            "description": "High quality for printing (2560px width, 95% quality)"
        },
        "compress_only": {
            "name": "Compress Only",
            "width": None,
            "height": None,
            "scale_percent": None,
            "quality": 85,
            "maintain_aspect": True,
            "description": "No resize, just compress (85% quality)"
        }
    }
    
    def __init__(self, config_file: str = CONFIG_FILE):
        """Initialize configuration manager."""
        self.config_file = Path(config_file)
        self.config = self.load_config()
    
    def load_config(self) -> Dict:
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠ Error loading config: {e}")
        return {}
    
    def save_config(self, config: Dict, name: str = "custom") -> bool:
        """Save configuration to file."""
        try:
            all_configs = self.load_config()
            all_configs[name] = config
            with open(self.config_file, 'w') as f:
                json.dump(all_configs, f, indent=2)
            print(f"✓ Configuration '{name}' saved to {self.config_file}")
            return True
        except Exception as e:
            print(f"✗ Error saving config: {e}")
            return False
    
    def list_configs(self) -> Dict:
        """List all available configurations."""
        configs = {}
        for key, preset in self.PRESETS.items():
            configs[key] = preset
        saved_configs = self.load_config()
        for key, config in saved_configs.items():
            if key not in configs:
                configs[key] = config
        return configs
    
    def get_config(self, name: str) -> Optional[Dict]:
        """Get a specific configuration by name."""
        if name in self.PRESETS:
            return self.PRESETS[name].copy()
        saved_configs = self.load_config()
        if name in saved_configs:
            return saved_configs[name]
        return None


def print_header():
    """Print application header."""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║   Image Resizer & Compressor - Pillow Edition                ║
║                  Hacktoberfest 2025 Project                   ║
╚═══════════════════════════════════════════════════════════════╝
    """)


def list_all_configurations(config_manager: ConfigManager):
    """List all available configurations."""
    print("\n" + "=" * 60)
    print("📋 AVAILABLE CONFIGURATIONS")
    print("=" * 60)
    
    print("\n🎁 PRESETS:")
    for key, preset in ConfigManager.PRESETS.items():
        print(f"\n  [{key}]")
        print(f"  Name: {preset['name']}")
        print(f"  {preset['description']}")
    
    saved_only = {k: v for k, v in config_manager.list_configs().items() if k not in ConfigManager.PRESETS}
    if saved_only:
        print("\n💾 SAVED CONFIGURATIONS:")
        for key, cfg in saved_only.items():
            print(f"\n  [{key}]")
            print(f"  Name: {cfg.get('name', key)}")
            if 'description' in cfg:
                print(f"  {cfg['description']}")
    else:
        print("\n💾 No saved configurations")
    
    print("\n" + "=" * 60)


def print_config(config: Dict):
    """Print configuration details."""
    print(f"Name: {config.get('name', 'Unnamed')}")
    if 'description' in config:
        print(f"Description: {config['description']}")
    
    if config.get('width'):
        print(f"Width: {config['width']}px")
    if config.get('height'):
        print(f"Height: {config['height']}px")
    if config.get('scale_percent'):
        print(f"Scale: {config['scale_percent']}%")
    if not config.get('width') and not config.get('height') and not config.get('scale_percent'):
        print("Resize: None (compress only)")
    
    print(f"Quality: {config.get('quality', 85)}%")
    print(f"Maintain Aspect Ratio: {config.get('maintain_aspect', True)}")


def process_images(ingest_dir: Path, output_dir: Path, config: Dict):
    """Process images with the given configuration."""
    print("\n" + "=" * 60)
    print("🚀 PROCESSING IMAGES")
    print("=" * 60)
    
    processor = ImageProcessor(str(ingest_dir), str(output_dir))
    
    successful, failed = processor.batch_process(
        width=config.get('width'),
        height=config.get('height'),
        scale_percent=config.get('scale_percent'),
        quality=config.get('quality', 85),
        maintain_aspect=config.get('maintain_aspect', True)
    )
    
    # Log results
    log_file = Path("processing_log.txt")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"""
{'='*60}
Processing Log - {timestamp}
{'='*60}
Configuration: {config.get('name', 'Unnamed')}
Width: {config.get('width', 'N/A')}
Height: {config.get('height', 'N/A')}
Scale: {config.get('scale_percent', 'N/A')}%
Quality: {config.get('quality', 85)}%
Results:
  Successful: {successful}
  Failed: {failed}
{'='*60}

"""
    
    try:
        with open(log_file, 'a') as f:
            f.write(log_entry)
        print(f"\n📝 Log saved to {log_file}")
    except Exception as e:
        print(f"⚠ Could not save log: {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Image Resizer & Compressor (Pillow Edition)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use a preset
  python3 cli_interface_pillow.py --config web
  
  # Custom parameters
  python3 cli_interface_pillow.py --width 800 --quality 85
  
  # Resize by percentage
  python3 cli_interface_pillow.py --scale 50 --quality 90
  
  # List all configurations
  python3 cli_interface_pillow.py --list-configs
        """
    )
    
    parser.add_argument('--ingest', '-i', default='./ingest', help='Input directory (default: ./ingest)')
    parser.add_argument('--output', '-o', default='./output', help='Output directory (default: ./output)')
    parser.add_argument('--config', '-c', help='Use a preset or saved configuration')
    parser.add_argument('--width', '-w', type=int, help='Target width in pixels')
    parser.add_argument('--height', '-H', type=int, help='Target height in pixels')
    parser.add_argument('--scale', '-s', type=int, help='Scale percentage')
    parser.add_argument('--quality', '-q', type=int, default=85, help='Compression quality 1-100 (default: 85)')
    parser.add_argument('--no-aspect', action='store_true', help='Do not maintain aspect ratio')
    parser.add_argument('--list-configs', action='store_true', help='List all available configurations')
    
    args = parser.parse_args()
    
    print_header()
    
    # Handle list configs
    if args.list_configs:
        config_manager = ConfigManager()
        list_all_configurations(config_manager)
        return
    
    ingest_dir = Path(args.ingest)
    output_dir = Path(args.output)
    
    print(f"📁 Ingest: {ingest_dir.absolute()}")
    print(f"📁 Output: {output_dir.absolute()}")
    
    # Get configuration
    if args.config:
        config_manager = ConfigManager()
        config = config_manager.get_config(args.config)
        
        if not config:
            print(f"❌ Configuration '{args.config}' not found")
            sys.exit(1)
        
        print(f"\n✓ Using configuration: {config.get('name', args.config)}")
    else:
        # Build config from arguments
        config = {
            "name": "Custom Configuration",
            "width": args.width,
            "height": args.height,
            "scale_percent": args.scale,
            "quality": args.quality,
            "maintain_aspect": not args.no_aspect
        }
        print("\n✓ Using command-line parameters")
    
    print_config(config)
    
    # Process
    process_images(ingest_dir, output_dir, config)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Process interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
