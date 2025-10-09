# Image Resizer Script

A command-line utility to quickly resize multiple images from a source folder and save them to a destination folder.

## Features

-   Batch resizes all `.jpg`, `.jpeg`, and `.png` images.
-   Creates the output directory if it doesn't already exist.
-   Simple and easy-to-use command-line interface.

## Prerequisites

-   Python 3.x
-   Pillow library

## Installation

1.  **Clone the repository** (or download the script).

2.  **Install the required library:**
    ```bash
    pip install Pillow
    ```

## Usage

Run the script from your terminal with the following structure:

```bash
python resize_images.py <input_folder> <output_folder> --size <WIDTH> <HEIGHT>