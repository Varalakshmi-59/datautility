from flask import Flask, request, render_template, redirect, url_for
import os
import psycopg2
import re
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from extract_telugu_words import extract_telugu_words  # Your word extraction logic

app = Flask(__name__)

# Path to your master list CSV
master_list_path = 'master_telugu_words.csv'

def extract_telugu_words(pdf_path):
    telugu_words = []

    try:
        # Step 1: Convert PDF pages to images (for OCR)
        print(f"Converting PDF: {pdf_path}")
        pages = convert_from_path(pdf_path)
        print(f"Total pages converted: {len(pages)}")

        # Step 2: Perform OCR and extract text from each page
        for i, page in enumerate(pages):
            print(f"Processing page {i + 1}")
            text = pytesseract.image_to_string(page, lang='tel')
            print(f"Extracted text from page {i + 1}: {text}")

            # Step 3: Use regex to find Telugu words
            words = re.findall(r'[\u0C00-\u0C7F]+', text)
            telugu_words += words
            print(f"Telugu words from page {i + 1}: {words}")

        if not telugu_words:
            print("No Telugu words found in the PDF.")

    except Exception as e:
        print(f"Error processing PDF: {e}")

    return list(set(telugu_words))  # Return unique words


# Database connection function
def connect_db():
    return psycopg2.connect(
        dbname='telugu_words_db',
        user='postgres',
        password='varam',  # Update with your password
        host='localhost',
        port='5432'
    )

# Function to check Telugu words and update the DB
def update_db_with_words(telugu_words):
    conn = connect_db()
    cur = conn.cursor()

    for word in telugu_words:
        cur.execute("SELECT count FROM unique_telugu_words WHERE word = %s", (word,))
        result = cur.fetchone()

        if result:
            new_count = result[0] + 1
            cur.execute("UPDATE unique_telugu_words SET count = %s WHERE word = %s", (new_count, word))
        else:
            cur.execute("INSERT INTO unique_telugu_words (word, count) VALUES (%s, 1)", (word,))
    
    conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'pdf_file' not in request.files:
        return "No file part", 400

    file = request.files['pdf_file']
    if file.filename == '':
        return "No selected file", 400

    pdf_path = os.path.join('/tmp', file.filename)
    file.save(pdf_path)

    telugu_words = extract_telugu_words(pdf_path)
    
    if not telugu_words:
        return "No Telugu words found in the PDF.", 400

    update_db_with_words(telugu_words)
    return redirect(url_for('view_master_list'))

@app.route('/view_counts')
def view_counts():
    conn = connect_db()
    cur = conn.cursor()
    
    cur.execute("SELECT LEFT(word, 1) AS letter, COUNT(*) FROM unique_telugu_words GROUP BY letter ORDER BY letter;")
    counts_by_letter = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM unique_telugu_words;")
    total_count = cur.fetchone()[0]

    cur.close()
    conn.close()
    
    return render_template('view_counts.html', counts_by_letter=counts_by_letter, total_count=total_count)

@app.route('/view_sorted_words')
def view_sorted_words():
    conn = connect_db()
    cur = conn.cursor()
    
    cur.execute("SELECT word FROM unique_telugu_words ORDER BY word;")
    sorted_words = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template('sorted_words.html', sorted_words=sorted_words)

@app.route('/add_word_form')
def add_word_form():
    return render_template('add_word.html')

@app.route('/add_word', methods=['POST'])
def add_word():
    new_word = request.form['word']
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("INSERT INTO unique_telugu_words (word, count) VALUES (%s, 1) ON CONFLICT (word) DO UPDATE SET count = unique_telugu_words.count + 1;", (new_word,))
    conn.commit()
    
    cur.close()
    conn.close()
    return redirect(url_for('view_sorted_words'))

@app.route('/check_word/<word>')
def check_word(word):
    conn = connect_db()
    cur = conn.cursor()
    
    cur.execute("SELECT count FROM unique_telugu_words WHERE word = %s", (word,))
    result = cur.fetchone()
    
    cur.close()
    conn.close()
    
    if result:
        return f"The word '{word}' exists in the database with a count of {result[0]}."
    else:
        return f"The word '{word}' does not exist in the database."

@app.route('/master_list')
def view_master_list():
    conn = connect_db()
    cur = conn.cursor()
    
    cur.execute("SELECT word, count FROM unique_telugu_words")
    words_with_counts = cur.fetchall()
    total_count = sum(count for _, count in words_with_counts)

    cur.close()
    conn.close()
    
    return render_template('master_list.html', words_with_counts=words_with_counts, total_count=total_count)

@app.route('/db_word_count')
def db_word_count():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT word, count FROM unique_telugu_words")
    words_with_count = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('word_count.html', words=words_with_count)

if __name__ == '__main__':
    app.run(debug=True)
