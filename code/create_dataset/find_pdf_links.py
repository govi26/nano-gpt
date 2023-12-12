import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse


def is_valid_url(url):
    # Check if the URL starts with http:// or https://
    return (
        url.startswith("/") or url.startswith("http://") or url.startswith("https://")
    )


def is_same_domain(url, base_domain):
    # Parse the URL to extract the domain
    domain = urlparse(url).netloc
    return (
        url.startswith("/")
        or domain == base_domain
        or domain.endswith("." + base_domain)
    )


def clean_url(url):
    # Remove query parameters from URL
    parsed_url = urlparse(url)
    # return urlunparse(parsed_url._replace(query=""))
    return url


def find_pdf_links(url, visited, base_url, output_file):
    # Convert relative URL to absolute URL
    url = urljoin(base_url, url)

    # Clean URL to remove query parameters
    cleaned_url = clean_url(url)

    # Check if URL is valid, within the same domain, and not visited
    if (
        not is_valid_url(url)
        or not is_same_domain(url, urlparse(base_url).netloc)
        or cleaned_url in visited
    ):
        return []

    visited.add(cleaned_url)

    # Send a request to the website
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"Error requesting {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # Find all hyperlinks on the page
    links = soup.find_all("a", href=True)

    pdf_links = []
    for link in links:
        href = link["href"]
        if (
            href is None
            or not is_valid_url(href)
            or not is_same_domain(href, urlparse(base_url).netloc)
        ):
            continue

        # Convert relative URL to absolute URL and clean it
        href = clean_url(urljoin(base_url, href))
        if href in visited:
            continue
        print(href)

        if href.endswith(".pdf"):
            pdf_links.append(href)
            output_file.write(href + "\n")
        elif href not in visited:
            # Recursively find PDFs in linked pages
            pdf_links.extend(find_pdf_links(href, visited, base_url, output_file))

    return pdf_links


visited_pages = set()
url = "https://www.nccn.org/guidelines/category_1"  # Replace with the target website
base_url = "https://nccn.org"
with open("pdf_links.txt", "w") as file:
    pdf_links = find_pdf_links(url, visited_pages, base_url, file)

# for link in pdf_links:
#     print(link)
