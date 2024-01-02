import PyPDF2
import os
import re

def main():
  pdf_directory = "./pdf_files"
  links_directory = "./pubmed_links"
  os.makedirs(links_directory, exist_ok=True)

  for filename in os.listdir(pdf_directory):
    if filename.endswith(".pdf"):
      pdf_path = os.path.join(pdf_directory, filename)
      urls = extract_urls_from_pdf(pdf_path)

      text_file_path = os.path.join(links_directory, f'{filename.replace(".pdf", ".txt")}')
      with open(text_file_path, "w") as text_file:
        for url in urls:
          text_file.write(url + "\n")

      print(f"Links extracted from {filename} to {text_file_path}")

def extract_urls_from_pdf(pdf_path):
  with open(pdf_path, "rb") as file:
    reader = PyPDF2.PdfReader(file)
    urls = []
    for page in reader.pages:
      text = page.extract_text()
      urls.extend(re.findall(r'https?://www\.ncbi\.nlm\.nih\.gov/pubmed/\d+', text))
    return urls

if __name__ == '__main__':
  main()
