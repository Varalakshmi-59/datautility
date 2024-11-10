import fitz  # PyMuPDF
import re

def extract_telugu_words(pdf_path):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    telugu_words = set()  # Use a set to avoid duplicates

    for page in doc:
        text = page.get_text()  # Extract text from the page
        # Use regex to find Telugu words
        telugu_words.update(re.findall(r'[\u0C00-\u0C7F]+', text))  # Unicode range for Telugu

    doc.close()
    return telugu_words

if __name__ == "__main__":
    pdf_path = '/mnt/c/users/likhi/downloads/telugutext.pdf'  # Adjust the path as necessary
    telugu_words = extract_telugu_words(pdf_path)

    # Print the extracted Telugu words
    print("Extracted Telugu Words:")
    for word in telugu_words:
        print(word)

    # Optional: Save the words to a CSV file
    import pandas as pd
    df = pd.DataFrame(list(telugu_words), columns=['Telugu Words'])
    df.to_csv('telugu_words.csv', index=False)
