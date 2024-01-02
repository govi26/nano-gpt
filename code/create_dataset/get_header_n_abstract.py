import csv
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed


def main():
  links_directory = "./pubmed_links"
  headers_n_abstracts_directory = "./headers_n_abstracts"

  for filename in os.listdir(links_directory):
    if filename.endswith(".txt"):
      links_filepath = os.path.join(links_directory, filename)

      with open(links_filepath, "r") as file:
        urls = file.read().splitlines()

        csv_file_path = os.path.join(headers_n_abstracts_directory, f'{filename.replace(".txt", ".csv")}')
        if Path(csv_file_path).exists():
          print(f'INFO: Ignoring as file - {csv_file_path} already exists.')
          continue
        with open(csv_file_path, mode="w", newline="", encoding="utf-8") as csv_file:
          csv_writer = csv.writer(csv_file)
          csv_writer.writerow(["Header", "Abstract", "URL"])

          with ThreadPoolExecutor() as executor:
            future_to_url = {executor.submit(scrape_header_and_abstract, url): url for url in urls}
            for future in as_completed(future_to_url):
              url = future_to_url[future]
              try:
                header, abstract = future.result()
                if header=="Error" or abstract=="Error":
                  print(f'Error: Skipping url: {url} in file: {filename}')
                elif header=="Not found" or abstract=="Not found":
                  print(f'Warning: Skipping url: {url} in file: {filename}')
                else:
                  csv_writer.writerow([header, abstract, url])
              except Exception as e:
                print(f'Error: Processing url- {url}: {str(e)}')

        print(f"Headers and abstracts have been written to {csv_file_path}")


def scrape_header_and_abstract(url):
  try:
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    header_selector = "h1.heading-title"
    abstract_selector = "div.abstract-content.selected"

    header_section = soup.select_one(header_selector)
    abstract_section = soup.select(abstract_selector + ' p')
    header, abstract = "Not found", "Not found"
    if header_section:
      header = soup.select_one(header_selector).get_text(strip=True)
    if abstract_section:
      abstract = ' '.join(paragraph.get_text(" ", strip=True) for paragraph in abstract_section)
    return header, abstract
  except requests.HTTPError as e:
    print(f"HTTP error occurred for URL {url}: {e}")
  except Exception as e:
    print(f"An error occurred for URL {url}: {e}")
  return "Error", "Error"


if __name__ == '__main__':
  main()
