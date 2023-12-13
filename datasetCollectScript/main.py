import os
import textract
import csv
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import download
import re

# Download NLTK resources (only needed once)
download('punkt')
download('stopwords')

def remove_stopwords(text, language='english'):
    stop_words = set(stopwords.words(language))
    words = word_tokenize(text)
    filtered_text = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered_text)

def clean_text(text):
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = ' '.join(text.split())
    return text

def extract_first_50_words(file_path):
    _, file_extension = os.path.splitext(file_path)
    if file_extension == '.pdf' or file_extension == '.docx' or file_extension == '.pptx':
        text = textract.process(file_path).decode('utf-8')
        words = text.split()[:50]
        return ' '.join(words)
    else:
        return None

def extract_and_label_documents(directory_path, output_csv):
    # Check if the CSV file exists
    is_existing_file = os.path.isfile(output_csv)

    with open(output_csv, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['text', 'label']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header only if the file is newly created
        if not is_existing_file:
            writer.writeheader()

        for filename in os.listdir(directory_path):
            if filename.endswith('.pdf') or filename.endswith('.docx') or filename.endswith('.pptx'):
                file_path = os.path.join(directory_path, filename)
                text = extract_first_50_words(file_path)
                if text:
                    # Remove English and Indonesian stopwords
                    text = remove_stopwords(text, 'english')
                    text = remove_stopwords(text, 'indonesian')

                    # Clean the text using the clean_text function
                    text = clean_text(text)

                    label = input(f"Label for {filename}: ")  # Manually input the label
                    writer.writerow({'text': text, 'label': label})

# Example Usage:
extract_and_label_documents("C:/Documents", "dataset.csv")
