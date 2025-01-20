from flask import Flask, request, render_template, redirect, url_for
import os
import psycopg2
from datetime import datetime
import csv
from extract_telugu_words import extract_telugu_words  # Ensure this import matches your file structure

app = Flask(__name__)

# Database connection function
def connect_db():
    return psycopg2.connect(
        dbname='telugu_words_db',
        user='postgres',
        password='varam',  # Update with your password
        host='localhost',
        port='5432'
    )

# Function to ensure a directory exists
def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to save extracted words to a CSV file
def save_words_to_csv(telugu_words, source_filename, output_directory='extracted_words'):
    # Ensure the output directory exists
    ensure_directory(output_directory)

    # Generate a unique filename for the CSV
    base_name = os.path.splitext(source_filename)[0]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_filename = f"{base_name}_words_{timestamp}.csv"
    output_path = os.path.join(output_directory, output_filename)

    # Write the words to the CSV file
    with open(output_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Word', 'Source'])  # Header row
        for entry in telugu_words:
            writer.writerow([entry['word'], entry['source']])

    print(f"Words saved to {output_path}")

# Function to update the database with extracted words
def update_db_with_words(telugu_words):
    conn = connect_db()
    cur = conn.cursor()

    for entry in telugu_words:
        word = entry['word']
        source = entry['source']

        # Check if word exists, and update or insert with source
        cur.execute("SELECT count, source FROM unique_telugu_words WHERE word = %s", (word,))
        result = cur.fetchone()

        if result:
            if result[1] != source:
                continue  # Skip if source is different
            new_count = result[0] + 1
            cur.execute("UPDATE unique_telugu_words SET count = %s WHERE word = %s", (new_count, word))
        else:
            cur.execute("INSERT INTO unique_telugu_words (word, count, source) VALUES (%s, 1, %s)", (word, source))

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

    # Save the uploaded file to a temporary location
    pdf_path = os.path.join('/tmp', file.filename)
    file.save(pdf_path)

    # Extract Telugu words from the PDF with the source filename
    words_with_source = extract_telugu_words(pdf_path, file.filename)

    if not words_with_source:
        return "No Telugu words found in the PDF.", 400

    # Save words to a CSV file
    save_words_to_csv(words_with_source, file.filename)

    # Update the database with the extracted words
    update_db_with_words(words_with_source)

    # Render master list template with extracted words
    return redirect(url_for('view_master_list'))

@app.route('/master_list')
def view_master_list():
    conn = connect_db()
    cur = conn.cursor()

    # Fetch words with their counts
    cur.execute("SELECT word, source, count FROM unique_telugu_words")
    words_with_counts = cur.fetchall()

    # Convert data for the template
    words_with_source = [{'word': word, 'source': source, 'count': count} for word, source, count in words_with_counts]

    # Calculate total word count
    total_word_count = sum(entry['count'] for entry in words_with_source)

    # Debug: Print the data being sent to the template
    print(words_with_source)

    cur.close()
    conn.close()

    return render_template('master_list.html', words_with_source=words_with_source, total_word_count=total_word_count)

if __name__ == '__main__':
    app.run(debug=True)
