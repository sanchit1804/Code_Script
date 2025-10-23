import os
from PyPDF2 import PdfReader

# Input and output folders
INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"

# Ensure output directory exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    """Extract all text from a single PDF file."""
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PdfReader(file)
            for page_num, page in enumerate(reader.pages):
                text += f"\n--- Page {page_num + 1} ---\n"
                text += page.extract_text() or ""
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return text

def process_all_pdfs():
    """Read all PDFs in input folder and save text to output folder."""
    pdf_files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print("No PDF files found in 'pdfs/' folder.")
        return

    for pdf_file in pdf_files:
        pdf_path = os.path.join(INPUT_FOLDER, pdf_file)
        txt_filename = os.path.splitext(pdf_file)[0] + ".txt"
        txt_path = os.path.join(OUTPUT_FOLDER, txt_filename)

        print(f"Processing {pdf_file}...")
        text = extract_text_from_pdf(pdf_path)

        with open(txt_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(text)

        print(f"Saved extracted text to {txt_path}")

if __name__ == "__main__":
    process_all_pdfs()
    