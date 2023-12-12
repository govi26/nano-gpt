import csv
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd


# Function to scrape header and abstract from a given URL
def scrape_header_and_abstract(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Replace the following selectors with the actual selectors for header and abstract on the web page
        header_selector = (
            "h1"  # Example selector, replace with actual selector for header
        )
        abstract_selector = "div.abstract"  # Example selector, replace with actual selector for abstract

        header = (
            soup.select_one(header_selector).get_text(strip=True)
            if soup.select_one(header_selector)
            else "Header Not Found"
        )
        abstract = (
            soup.select_one(abstract_selector).get_text(strip=True)
            if soup.select_one(abstract_selector)
            else "Abstract Not Found"
        )

        return header, abstract
    except requests.HTTPError as e:
        print(f"HTTP error occurred for URL {url}: {e}")
    except Exception as e:
        print(f"An error occurred for URL {url}: {e}")

    return "Error", "Error"


# Directory containing the text files with links
links_directory = "./pubmed-links"
# CSV file to save the headers and abstracts
csv_filename = "./headers_and_abstracts.csv"

# Prepare the CSV file with headers
with open(csv_filename, mode="w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["PDF Name", "URL", "Header", "Abstract"])

    # Iterate over all text files in the directory
    for filename in os.listdir(links_directory):
        if filename.endswith("_links.txt"):
            pdf_name = filename.replace("_links.txt", "")
            links_filepath = os.path.join(links_directory, filename)

            with open(links_filepath, "r") as file:
                urls = file.read().splitlines()

                # Scrape each URL
                for url in urls:
                    header, abstract = scrape_header_and_abstract(url)
                    csv_writer.writerow([pdf_name, url, header, abstract])

print(f"Headers and abstracts have been written to {csv_filename}")
