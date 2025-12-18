import fitz  # PyMuPDF
import re

def clean_bible_pdf(input_pdf, output_txt):
    # Regex to find numbers at the start of lines or within text
    # This matches digits followed by optional spaces
    number_pattern = re.compile(r'\d+\s*')

    try:
        # Open the PDF
        doc = fitz.open(input_pdf)
        cleaned_content = []

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text("text")
            
            # Remove the numbers using regex
            cleaned_text = number_pattern.sub('', text)
            cleaned_content.append(cleaned_text)

        # Save to a text file
        with open(output_txt, 'w', encoding='utf-8') as f:
            f.write("\n".join(cleaned_content))
            
        print(f"Success! Cleaned text saved to {output_txt}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Usage
clean_bible_pdf("Genesisy.pdf", "cleaned_bible.txt")