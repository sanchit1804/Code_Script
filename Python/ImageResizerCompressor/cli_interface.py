#!/usr/bin/env python3
"""
Enhanced Image Resizer & Compressor with CLI Configuration
==========================================================
Advanced version with dedicated ingest folder and configurable CLI interface.

Features:
- Dedicated ingest folder for input images
- Save and load processing configurations
- Command-line arguments support
- Interactive configuration mode
- Preset configurations (web, social media, email, thumbnails)
- Watch folder mode for automatic processing

Author: Hacktoberfest 2025 Contributor
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
from image_resizer_compressor import ImageProcessor


class ConfigManager:
    """Manages configuration presets and user settings."""
    
    CONFIG_FILE = "config.json"
    
    # Preset configurations
    PRESETS = {
        "web": {
            "name": "Web Optimization",
            "method": "pillow",
            "width": 1920,
            "height": None,
            "scale_percent": None,
            "quality": 85,
            "maintain_aspect": True,
            "description": "Optimized for web pages (1920px width, 85% quality)"
        },
        "social": {
            "name": "Social Media",
            "method": "pillow",
            "width": 1080,
            "height": 1080,
            "scale_percent": None,
            "quality": 90,
            "maintain_aspect": False,
            "description": "Square format for Instagram/Facebook (1080x1080)"
        },
        "email": {
            "name": "Email Attachments",
            "method": "pillow",
            "width": None,
            "height": None,
            "scale_percent": 40,
            "quality": 80,
            "maintain_aspect": True,
            "description": "Compressed for email (40% of original, 80% quality)"
        },
        "thumbnail": {
            "name": "Thumbnails",
            "method": "pillow",
            "width": 200,
            "height": None,
            "scale_percent": None,
            "quality": 75,
            "maintain_aspect": True,
            "description": "Small thumbnails (200px width, 75% quality)"
        },
        "high_quality": {
            "name": "High Quality",
            "method": "pillow",
            "width": 2560,
            "height": None,
            "scale_percent": None,
            "quality": 95,
            "maintain_aspect": True,
            "description": "High quality for printing (2560px width, 95% quality)"
        },
        "compress_only": {
            "name": "Compress Only",
            "method": "pillow",
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
        """List all available configurations (presets + saved)."""
        configs = {}
        
        # Add presets
        for key, preset in self.PRESETS.items():
            configs[key] = preset
        
        # Add saved configs
        saved_configs = self.load_config()
        for key, config in saved_configs.items():
            if key not in configs:  # Don't override presets
                configs[key] = config
        
        return configs
    
    def get_config(self, name: str) -> Optional[Dict]:
        """Get a specific configuration by name."""
        # Check presets first
        if name in self.PRESETS:
            return self.PRESETS[name].copy()
        
        # Check saved configs
        saved_configs = self.load_config()
        if name in saved_configs:
            return saved_configs[name]
        
        return None
    
    def delete_config(self, name: str) -> bool:
        """Delete a saved configuration."""
        if name in self.PRESETS:
            print(f"⚠ Cannot delete preset configuration: {name}")
            return False
        
        try:
            all_configs = self.load_config()
            if name in all_configs:
                del all_configs[name]
                with open(self.config_file, 'w') as f:
                    json.dump(all_configs, f, indent=2)
                print(f"✓ Configuration '{name}' deleted")
                return True
            else:
                print(f"⚠ Configuration '{name}' not found")
                return False
        except Exception as e:
            print(f"✗ Error deleting config: {e}")
            return False


def print_header():
    """Print application header."""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║   Enhanced Image Resizer & Compressor - CLI Configuration   ║
║                  Hacktoberfest 2025 Project                   ║
╚═══════════════════════════════════════════════════════════════╝
    """)


def interactive_mode():
    """Run interactive configuration mode."""
    print_header()
    
    config_manager = ConfigManager()
    
    print("\n📋 INTERACTIVE CONFIGURATION MODE\n")
    print("=" * 60)
    
    # Show current folder setup
    ingest_dir = Path("./ingest")
    output_dir = Path("./output")
    
    print(f"📁 Ingest Folder: {ingest_dir.absolute()}")
    print(f"📁 Output Folder: {output_dir.absolute()}")
    print("=" * 60)
    
    # Check for images in ingest folder
    processor = ImageProcessor(str(ingest_dir), str(output_dir))
    image_files = processor.get_image_files()
    
    if not image_files:
        print(f"\n⚠ No images found in {ingest_dir}")
        print("   Please add images to the ingest folder and try again.")
        return
    
    print(f"\n✓ Found {len(image_files)} image(s) to process:")
    for img in image_files[:5]:  # Show first 5
        print(f"  - {img.name}")
    if len(image_files) > 5:
        print(f"  ... and {len(image_files) - 5} more")
    
    print("\n" + "=" * 60)
    print("📋 CHOOSE CONFIGURATION METHOD")
    print("=" * 60)
    print("1. Use a preset configuration")
    print("2. Create custom configuration")
    print("3. Load saved configuration")
    print("4. List all configurations")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    config = None
    config_name = None
    
    if choice == "1":
        # Use preset
        print("\n📦 AVAILABLE PRESETS:")
        print("=" * 60)
        presets = ConfigManager.PRESETS
        for i, (key, preset) in enumerate(presets.items(), 1):
            print(f"{i}. {preset['name']}")
            print(f"   {preset['description']}")
            print()
        
        preset_choice = input(f"Choose preset (1-{len(presets)}): ").strip()
        try:
            preset_idx = int(preset_choice) - 1
            preset_key = list(presets.keys())[preset_idx]
            config = presets[preset_key].copy()
            config_name = preset_key
            print(f"\n✓ Using preset: {config['name']}")
        except (ValueError, IndexError):
            print("❌ Invalid choice")
            return
    
    elif choice == "2":
        # Custom configuration
        config = create_custom_config()
        config_name = "custom"
        
        # Ask to save
        save_choice = input("\n💾 Save this configuration? (y/n): ").strip().lower()
        if save_choice == 'y':
            name = input("Enter configuration name: ").strip()
            if name:
                config_manager.save_config(config, name)
    
    elif choice == "3":
        # Load saved configuration
        all_configs = config_manager.list_configs()
        saved_only = {k: v for k, v in all_configs.items() if k not in ConfigManager.PRESETS}
        
        if not saved_only:
            print("\n⚠ No saved configurations found")
            return
        
        print("\n💾 SAVED CONFIGURATIONS:")
        print("=" * 60)
        for i, (key, cfg) in enumerate(saved_only.items(), 1):
            print(f"{i}. {cfg.get('name', key)}")
            if 'description' in cfg:
                print(f"   {cfg['description']}")
            print()
        
        config_choice = input(f"Choose configuration (1-{len(saved_only)}): ").strip()
        try:
            config_idx = int(config_choice) - 1
            config_key = list(saved_only.keys())[config_idx]
            config = saved_only[config_key]
            config_name = config_key
            print(f"\n✓ Loaded configuration: {config.get('name', config_key)}")
        except (ValueError, IndexError):
            print("❌ Invalid choice")
            return
    
    elif choice == "4":
        # List all configurations
        list_all_configurations(config_manager)
        return
    
    else:
        print("❌ Invalid choice")
        return
    
    if config:
        # Confirm and process
        print("\n" + "=" * 60)
        print("📊 CONFIGURATION SUMMARY")
        print("=" * 60)
        print_config(config)
        
        confirm = input("\n▶ Start processing with this configuration? (y/n): ").strip().lower()
        if confirm == 'y':
            process_images(ingest_dir, output_dir, config)
        else:
            print("❌ Processing cancelled")


def create_custom_config() -> Dict:
    """Create a custom configuration interactively."""
    print("\n🔧 CUSTOM CONFIGURATION")
    print("=" * 60)
    
    config = {
        "name": "Custom Configuration",
        "description": "User-defined custom settings"
    }
    
    # Method
    print("\nProcessing Method:")
    print("1. Pillow (recommended)")
    print("2. OpenCV")
    method_choice = input("Choose method (1 or 2): ").strip()
    config["method"] = "opencv" if method_choice == "2" else "pillow"
    
    # Resize option
    print("\nResize Option:")
    print("1. By width (maintain aspect ratio)")
    print("2. By height (maintain aspect ratio)")
    print("3. By percentage")
    print("4. Custom dimensions (width x height)")
    print("5. Compress only (no resize)")
    
    resize_choice = input("Choose option (1-5): ").strip()
    
    config["width"] = None
    config["height"] = None
    config["scale_percent"] = None
    config["maintain_aspect"] = True
    
    try:
        if resize_choice == "1":
            config["width"] = int(input("Enter target width (px): "))
        elif resize_choice == "2":
            config["height"] = int(input("Enter target height (px): "))
        elif resize_choice == "3":
            config["scale_percent"] = int(input("Enter scale percentage (e.g., 50): "))
        elif resize_choice == "4":
            config["width"] = int(input("Enter target width (px): "))
            config["height"] = int(input("Enter target height (px): "))
            config["maintain_aspect"] = False
        # Option 5: no resize
    except ValueError:
        print("⚠ Invalid input, using default values")
    
    # Quality
    try:
        quality = int(input("\nEnter compression quality (1-100, recommended 85): ") or "85")
        config["quality"] = max(1, min(100, quality))
    except ValueError:
        config["quality"] = 85
    
    return config


def print_config(config: Dict):
    """Print configuration details."""
    print(f"Name: {config.get('name', 'Unnamed')}")
    if 'description' in config:
        print(f"Description: {config['description']}")
    print(f"Method: {config.get('method', 'pillow').upper()}")
    
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


def list_all_configurations(config_manager: ConfigManager):
    """List all available configurations."""
    print("\n" + "=" * 60)
    print("📋 ALL CONFIGURATIONS")
    print("=" * 60)
    
    all_configs = config_manager.list_configs()
    
    # Presets
    print("\n🎁 PRESETS:")
    for key, preset in ConfigManager.PRESETS.items():
        print(f"\n  [{key}]")
        print(f"  Name: {preset['name']}")
        print(f"  {preset['description']}")
    
    # Saved configs
    saved_only = {k: v for k, v in all_configs.items() if k not in ConfigManager.PRESETS}
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


def process_images(ingest_dir: Path, output_dir: Path, config: Dict):
    """Process images with the given configuration."""
    print("\n" + "=" * 60)
    print("🚀 PROCESSING IMAGES")
    print("=" * 60)
    
    processor = ImageProcessor(str(ingest_dir), str(output_dir))
    
    # Extract config parameters
    method = config.get('method', 'pillow')
    width = config.get('width')
    height = config.get('height')
    scale_percent = config.get('scale_percent')
    quality = config.get('quality', 85)
    maintain_aspect = config.get('maintain_aspect', True)
    
    # Process
    successful, failed = processor.batch_process(
        method=method,
        width=width,
        height=height,
        scale_percent=scale_percent,
        quality=quality,
        maintain_aspect=maintain_aspect
    )
    
    # Log results
    log_processing(config, successful, failed)


def log_processing(config: Dict, successful: int, failed: int):
    """Log processing results to a file."""
    log_file = Path("processing_log.txt")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"""
{'='*60}
Processing Log - {timestamp}
{'='*60}
Configuration: {config.get('name', 'Unnamed')}
Method: {config.get('method', 'pillow')}
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


def cli_mode(args):
    """Run in CLI mode with arguments."""
    print_header()
    
    ingest_dir = Path(args.ingest)
    output_dir = Path(args.output)
    
    print(f"📁 Ingest: {ingest_dir.absolute()}")
    print(f"📁 Output: {output_dir.absolute()}")
    
    # Check if using a preset or saved config
    if args.config:
        config_manager = ConfigManager()
        config = config_manager.get_config(args.config)
        
        if not config:
            print(f"❌ Configuration '{args.config}' not found")
            sys.exit(1)
        
        print(f"\n✓ Using configuration: {config.get('name', args.config)}")
        print_config(config)
    else:
        # Build config from arguments
        config = {
            "method": args.method,
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


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Image Resizer & Compressor with CLI Configuration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (recommended)
  python cli_interface.py
  
  # Use a preset
  python cli_interface.py --config web
  
  # Custom parameters
  python cli_interface.py --width 800 --quality 85
  
  # Resize by percentage
  python cli_interface.py --scale 50 --quality 90
  
  # List all configurations
  python cli_interface.py --list-configs
        """
    )
    
    parser.add_argument(
        '--ingest', '-i',
        default='./ingest',
        help='Input directory (default: ./ingest)'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='./output',
        help='Output directory (default: ./output)'
    )
    
    parser.add_argument(
        '--config', '-c',
        help='Use a preset or saved configuration (e.g., web, social, email)'
    )
    
    parser.add_argument(
        '--method', '-m',
        choices=['pillow', 'opencv'],
        default='pillow',
        help='Processing method (default: pillow)'
    )
    
    parser.add_argument(
        '--width', '-w',
        type=int,
        help='Target width in pixels'
    )
    
    parser.add_argument(
        '--height', '-H',
        type=int,
        help='Target height in pixels'
    )
    
    parser.add_argument(
        '--scale', '-s',
        type=int,
        help='Scale percentage (e.g., 50 for 50%%)'
    )
    
    parser.add_argument(
        '--quality', '-q',
        type=int,
        default=85,
        help='Compression quality 1-100 (default: 85)'
    )
    
    parser.add_argument(
        '--no-aspect',
        action='store_true',
        help='Do not maintain aspect ratio'
    )
    
    parser.add_argument(
        '--list-configs',
        action='store_true',
        help='List all available configurations'
    )
    
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )
    
    args = parser.parse_args()
    
    # Handle special commands
    if args.list_configs:
        config_manager = ConfigManager()
        list_all_configurations(config_manager)
        return
    
    # Check if any processing arguments provided
    has_args = any([
        args.config,
        args.width,
        args.height,
        args.scale,
        args.quality != 85  # Non-default quality
    ])
    
    # Run appropriate mode
    if args.interactive or not has_args:
        interactive_mode()
    else:
        cli_mode(args)


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
