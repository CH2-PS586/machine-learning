import os
import textract
import csv


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
                label = input(f"Label for {filename}: ")  # Manually input the label
                writer.writerow({'text': text, 'label': label})

# Example Usage:
extract_and_label_documents("D:/UNSRI/BANGKIT", "dataset.csv")