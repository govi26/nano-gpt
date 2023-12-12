import PyPDF2
import os
import re


# Function to extract URLs from a PDF file
def extract_urls_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        urls = []
        for page in reader.pages:
            text = page.extract_text()
            # Find all web links
            urls.extend(re.findall(r"https?://\S+|www\.\S+", text))
        return urls


# Directory containing your PDF files
pdf_directory = "./pdf_files"
# Directory where you want to save the text files with links
links_directory = "./pubmed_links"

# Ensure the directory for links exists
os.makedirs(links_directory, exist_ok=True)

output_file = "file.txt"

# Iterate over all PDFs in the directory
for filename in os.listdir(pdf_directory):
    if filename.endswith(".pdf"):
        # Extract the base name of the PDF file to use as the text file name
        base_name = os.path.splitext(filename)[0]
        pdf_path = os.path.join(pdf_directory, filename)
        urls = extract_urls_from_pdf(pdf_path)

        # Write the URLs to a text file
        text_file_path = os.path.join(links_directory, output_file)
        with open(text_file_path, "w") as text_file:
            for url in urls:
                text_file.write(url + "\n")

        print(f"Links extracted from {filename} to {text_file_path}")
