from PIL import Image
import pytesseract
import fitz  # PyMuPDF
import re


def extract_telugu_words(pdf_path, source_file):
    telugu_words = []
    telugu_pattern = re.compile(r'[\u0C00-\u0C7F]+')  # Regex pattern for Telugu script

    try:
        doc = fitz.open(pdf_path)

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text()  # Extract text from the page

            if not text:  # If no text is extracted, fall back to OCR
                print(f"No text extracted from page {page_num + 1}, using OCR.")
                pix = page.get_pixmap()  # Convert page to image
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                text = pytesseract.image_to_string(img, lang='tel')  # Perform OCR for Telugu text

            # Log the extracted text
            print(f"Text from page {page_num + 1}: {text[:500]}")  # Preview text

            # Find Telugu words in the extracted text
            words = telugu_pattern.findall(text)
            print(f"Telugu words found on page {page_num + 1}: {words}")  # Log the extracted words

            for word in words:
                telugu_words.append({'word': word, 'source': source_file})

        doc.close()
    except Exception as e:
        print(f"Error processing file {source_file}: {e}")

    return telugu_words
