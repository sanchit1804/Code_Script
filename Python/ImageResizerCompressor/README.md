# 📸 Image Resizer & Compressor

A powerful Python tool for **bulk image resizing and compression**. Reduce file sizes while maintaining quality - perfect for web optimization, social media, email attachments, and storage management.

## ✨ Features

- 🔄 **Bulk Processing** - Process multiple images simultaneously
- 🎁 **6 Built-in Presets** - web, social, email, thumbnail, high_quality, compress_only
- 📁 **Organized Workflow** - Dedicated ingest (input) and output folders
- 📏 **Flexible Resizing** - By width, height, percentage, or custom dimensions
- 🗜️ **Smart Compression** - Quality control (1-100), typically 48%+ file size reduction
- 🎨 **Multiple Formats** - JPG, PNG, BMP, WEBP, TIFF
- 📊 **Detailed Statistics** - Track size reduction for each image
- 📝 **Processing Log** - Automatic history tracking
- ⚡ **Aspect Ratio Preservation** - Optional automatic maintenance
- 🎛️ **Dual Interface** - CLI with arguments or interactive mode

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install Pillow

# 2. Add images to ingest folder
cp ~/Pictures/*.jpg ingest/

# 3. Process with a preset
python3 cli_interface_pillow.py --config email

# 4. Get results from output folder
ls -lh output/
```

## 📋 Prerequisites

- **Python 3.6+**
- **Pillow** (required) - Primary image processing library
- **OpenCV** (optional) - Only for advanced features
- **NumPy** (optional) - Only needed with OpenCV

## 🔧 Installation

### Minimal Setup (Recommended)
```bash
# Install Pillow only (lightweight, works for 95% of use cases)
pip install Pillow
```

### Full Setup (Optional)
```bash
# Install all dependencies for advanced features
pip install -r requirements.txt
```

## 💻 Usage

### Using CLI with Presets (Easiest)

```bash
# Web optimization (1920px wide, 85% quality)
python3 cli_interface_pillow.py --config web

# Email attachments (40% scale, perfect for email)
python3 cli_interface_pillow.py --config email

# Social media squares (1080x1080 for Instagram)
python3 cli_interface_pillow.py --config social

# Thumbnails (200px wide, 75% quality)
python3 cli_interface_pillow.py --config thumbnail

# High quality (2560px, 95% quality for printing)
python3 cli_interface_pillow.py --config high_quality

# Compress only (no resize, just compression)
python3 cli_interface_pillow.py --config compress_only
```

### Using Custom Parameters

```bash
# Resize to specific width
python3 cli_interface_pillow.py --width 800 --quality 85

# Resize by percentage
python3 cli_interface_pillow.py --scale 50 --quality 90

# Specific dimensions (may distort)
python3 cli_interface_pillow.py --width 1024 --height 768 --no-aspect

# Custom input/output folders
python3 cli_interface_pillow.py --ingest ~/Photos --output ~/Compressed --config web

# List all available presets
python3 cli_interface_pillow.py --list-configs
```

### Interactive Mode

```bash
# Original interactive script with step-by-step prompts
python3 image_resizer_compressor.py
```

## 📊 Available Presets

| Preset | Dimensions | Quality | Best For |
|--------|------------|---------|----------|
| **web** | 1920px width | 85% | Websites, blogs |
| **social** | 1080x1080 | 90% | Instagram, Facebook |
| **email** | 40% of original | 80% | Email attachments |
| **thumbnail** | 200px width | 75% | Thumbnails, previews |
| **high_quality** | 2560px width | 95% | Printing, professional |
| **compress_only** | No resize | 85% | Size reduction only |

## 📁 Project Structure

```
ImageResizerCompressor/
├── cli_interface_pillow.py      # CLI version (Pillow only) ⭐ Recommended
├── cli_interface.py              # CLI version (with OpenCV support)
├── image_resizer_compressor.py  # Original interactive version
├── ingest/                       # Input folder - place images here
├── output/                       # Output folder - processed images saved here
├── config.json                   # Saved preset configurations
├── requirements.txt              # Python dependencies
├── example_usage.py              # Programmatic usage examples
├── test_setup.py                 # Setup testing script
├── test_pillow_only.py           # Pillow-only validation
├── demo_cli.sh                   # Demo script
└── README.md                     # This file
```

## 📝 Detailed Examples

### Example 1: Optimize for Web
```bash
# Add images
cp ~/Downloads/photos/*.jpg ingest/

# Process for web (1920px, 85% quality)
python3 cli_interface_pillow.py --config web

# Results
# Original: 3024x4032 (2458 KB)
# Output:   1920x2560 (856 KB)
# Savings:  65.2%
```

### Example 2: Prepare for Email
```bash
# Best compression for email
python3 cli_interface_pillow.py --config email

# Results
# Original: 1920x1080 (1234 KB)
# Output:   768x432 (412 KB)
# Savings:  66.6%
```

### Example 3: Create Instagram Posts
```bash
# Make square images for Instagram
python3 cli_interface_pillow.py --config social

# Results
# Original: 4000x3000 (3567 KB)
# Output:   1080x1080 (687 KB)
# Savings:  80.7%
```

### Example 4: Custom Resize
```bash
# Resize to 800px width with 90% quality
python3 cli_interface_pillow.py --width 800 --quality 90

# Or resize to 50% of original size
python3 cli_interface_pillow.py --scale 50 --quality 85
```

## 🎯 Command-Line Arguments

```
--ingest, -i      Input directory (default: ./ingest)
--output, -o      Output directory (default: ./output)
--config, -c      Use a preset configuration
--width, -w       Target width in pixels
--height, -H      Target height in pixels
--scale, -s       Scale percentage (e.g., 50)
--quality, -q     Compression quality 1-100 (default: 85)
--no-aspect       Don't maintain aspect ratio
--list-configs    List all available presets
--help            Show help message
```

## 📊 Expected Results

### Compression Performance
- **Web preset:** 60-70% file size reduction
- **Email preset:** 50-60% file size reduction  
- **Social preset:** 75-85% file size reduction
- **Thumbnail preset:** 95%+ file size reduction

### Processing Speed
- ~100-200 ms per image (depending on size and complexity)
- Batch processing of 100 images: ~20-30 seconds

## 🔧 Workflow

```
1. Drop images → ingest/
2. Run command → python3 cli_interface_pillow.py --config PRESET
3. Get results → output/
4. Check log → processing_log.txt
```

## 🎓 Which Script to Use?

| Script | Use When | Dependencies |
|--------|----------|--------------|
| **cli_interface_pillow.py** ⭐ | General use, CLI with presets | Pillow only |
| cli_interface.py | Need OpenCV features | Pillow + OpenCV |
| image_resizer_compressor.py | Prefer interactive prompts | Pillow + OpenCV |

**Recommendation:** Start with `cli_interface_pillow.py` - it's lightweight and handles most use cases!

## 🔍 Quality Settings Guide

| Quality | File Size | Visual Quality | Use Case |
|---------|-----------|----------------|----------|
| 95-100 | Largest | Perfect | Professional photography |
| **85-94** | **Medium** | **Excellent** | **Web images (recommended)** |
| 70-84 | Small | Good | Social media |
| 50-69 | Smaller | Acceptable | Thumbnails |
| 1-49 | Tiny | Poor | Not recommended |

## 🔥 Real-World Test Results

Tested with 19 PNG screenshots (1920x1080):
- **Original size:** 1.2 MB
- **After email preset:** 616 KB  
- **Compression:** 48.7% file size reduction
- **Success rate:** 100% (19/19 images)
- **Processing time:** ~2 seconds

## 🆘 Troubleshooting

### No images found
```bash
# Check if images are in ingest folder
ls ingest/

# Supported formats: JPG, PNG, BMP, WEBP, TIFF
```

### Module not found error
```bash
# Install Pillow
pip install Pillow

# Or install all dependencies
pip install -r requirements.txt
```

### Permission denied
```bash
# Make script executable
chmod +x cli_interface_pillow.py demo_cli.sh
```

### Poor quality results
```bash
# Increase quality setting
python3 cli_interface_pillow.py --config high_quality

# Or specify custom quality
python3 cli_interface_pillow.py --width 800 --quality 95
```

## 📝 Processing Log

Every run is automatically logged to `processing_log.txt`:

```
============================================================
Processing Log - 2025-10-05 14:30:15
============================================================
Configuration: Email Attachments
Width: None
Height: None
Scale: 40%
Quality: 80%
Results:
  Successful: 19
  Failed: 0
============================================================
```

View the log:
```bash
cat processing_log.txt
```

## 🎯 Use Cases

1. **Web Development** - Optimize images for faster page loads
2. **Social Media** - Create platform-specific image sizes
3. **Email Marketing** - Reduce attachment sizes
4. **E-commerce** - Generate product thumbnails
5. **Photography** - Batch process photo collections
6. **Mobile Apps** - Reduce app asset sizes
7. **Storage Management** - Free up disk space

## 🤝 Contributing

Contributions are welcome! This is a **Hacktoberfest 2025** project.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - feel free to use it for personal or commercial projects!

## 👨‍💻 Author

Created as part of **Hacktoberfest 2025** contribution to the [Code_Script](https://github.com/Spartan1-1-7/Code_Script) repository.

## 🌟 Acknowledgments

- **Pillow** community for excellent image processing library
- **OpenCV** community for advanced computer vision features
- **Hacktoberfest 2025** for the opportunity
- All contributors and users

## 📞 Support

- 📖 Read this README for detailed usage
- 🐛 [Report issues](https://github.com/Spartan1-1-7/Code_Script/issues)
- ⭐ Star the repo if you find it helpful!

---

## 🚀 Quick Reference

```bash
# Most common commands

# List presets
python3 cli_interface_pillow.py --list-configs

# Web optimization
python3 cli_interface_pillow.py --config web

# Email compression (best compression!)
python3 cli_interface_pillow.py --config email

# Custom width (800px)
python3 cli_interface_pillow.py --width 800 --quality 85

# Resize to 50% of original
python3 cli_interface_pillow.py --scale 50

# Get help
python3 cli_interface_pillow.py --help
```

---

**Happy Image Processing! 📸✨**

*Built with ❤️ for Hacktoberfest 2025*

**If you find this helpful, please ⭐ star the repository!**
