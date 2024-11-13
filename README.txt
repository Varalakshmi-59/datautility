# Data Utility for Word Lists in Indian Languages
This project is a Flask-based application designed to extract, process, and manage Telugu words from PDF files. The tool uses OCR (Optical Character Recognition) to scan PDFs for Telugu words and stores them in a PostgreSQL database for analysis and management. Users can upload PDFs, view word counts, search for words, and add new words manually.
## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Routes](#routes)
- [Database Schema](#database-schema)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)
---
## Project Overview
This utility helps in extracting and organizing Telugu words, making it easier to create a master word list. The extracted words are stored in a PostgreSQL database with frequency counts for each word. It supports the following actions:
- PDF file upload for word extraction
- Sorting and viewing of extracted Telugu words
- Manual word addition with a frequency count
---
## Features
- **PDF Upload and Telugu Word Extraction**: Users can upload PDFs, which are processed to extract Telugu words.
- **Database Integration**: All extracted words are stored in a PostgreSQL database.
- **User Operations**:
  - View words and their counts.
  - Add new words manually.
  - View total word count and counts by the first letter.
  ---
## Installation
### Prerequisites
- **Python** (version 3.8+ recommended)
- **PostgreSQL** (setup required with a `telugu_words_db` database)
- **Tesseract OCR** (for OCR processing)
Step 1: Clone the Repository

git clone https://github.com/yourusername/data-utility-for-telugu-words.git
cd  data-utility-for-telugu-words
Step 2: Install Dependencies
* Install project dependencies:
* pip install -r requirements.txt
* Install Tesseract OCR:
* Windows: Download from Tesseract OCR GitHub.
* Linux: Run sudo apt install tesseract-ocr.
* Mac: Run brew install tesseract.
Step 3: Database Setup
Create a PostgreSQL database:
* CREATE DATABASE telugu_words_db;
Create the unique_telugu_words table:
CREATE TABLE unique_telugu_words (
    word VARCHAR PRIMARY KEY,
    count INTEGER DEFAULT 1
);
Step 4: Configure Database Connection
* Update database credentials in the connect_db() function within your Flask app.
Step 5: Run the Application
* flask run
* Access the application at http://127.0.0.1:5000.
Usage
* Upload a PDF: Go to the /upload route and upload a PDF for word extraction.
* View Words and Counts:
* Visit /view_counts to see word counts grouped by the first letter.
* Visit /view_sorted_words to see all words in alphabetical order.
* Add a Word Manually: Use the /add_word_form to add new Telugu words manually.
* Check Word Existence: Use /check_word/<word> to check if a word exists in the database.
Routes
* / - Home page
* /upload - Upload a PDF and extract words
* /view_counts - View word counts grouped by the first letter
* /view_sorted_words - View all words alphabetically
* /add_word_form - Form to add new words
* /add_word - Endpoint to add new words
* /check_word/<word> - Check the database for a specific word
* /master_list - View the master list of words with counts
Database Schema
* Table: unique_telugu_words
* Columns:
		1.word (VARCHAR, Primary Key): Stores unique Telugu words.
		2.count (INTEGER): Stores the frequency count for each word.
Troubleshooting
* Database Connection Issues:
* Check the database credentials in the connect_db() function.
* Ensure PostgreSQL is running and accessible.
* OCR Issues:
* Verify Tesseract OCR is installed and added to the PATH.
* If text extraction accuracy is low, ensure the PDF quality is high and that the lang='tel' argument in pytesseract is set correctly.
* File Access on WSL:
* To access WSL files on Windows, use the \\wsl$\ network path or run explorer.exe . from your WSL terminal.
Future Improvements
* Multi-language Support: Expand to support more Indian languages.
* Advanced Sorting and Filtering: Add more filters and sorting options.
* User Authentication: Secure routes for managing the word list.
* Bulk PDF Uploads: Allow multiple PDFs to be processed at once.
