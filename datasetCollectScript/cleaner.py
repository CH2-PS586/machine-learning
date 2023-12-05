import csv
import re

def clean_text(text):
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = ' '.join(text.split())
    return text

def clean_and_rewrite_csv(input_csv, output_csv):
    with open(input_csv, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames

        # Check if 'text' and 'label' columns are present
        if 'text' not in fieldnames or 'label' not in fieldnames:
            print("Error: 'text' and 'label' columns are required in the input CSV.")
            return

        rows = []
        for row in reader:
            # Clean the text before writing to CSV
            cleaned_text = clean_text(row['text'])
            row['text'] = cleaned_text
            rows.append(row)

    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

# Example Usage:
clean_and_rewrite_csv("dataset.csv", "dataset_cleaned.csv")