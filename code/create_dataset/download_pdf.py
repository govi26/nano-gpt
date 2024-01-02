from selenium import webdriver
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse


# Replace these with your login credentials and the target URL
login_url = "https://www.nccn.org/login"  # URL of the login page
home_url = "https://www.nccn.org/home"  # URL of the login page

pdf_url = "https://nccn.org/professionals/physician_gls/pdf/prostate_harmonized-caribbean.pdf"  # URL of the PDF to download
username = "<username>"
password = "<password>"

download_directory = "/Users/govindyadav/nano-gpt/code/create_dataset/pdf_files"
chrome_options = Options()
prefs = {
    "download.default_directory": download_directory,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True  # It will not show PDF directly in chrome
}
chrome_options.add_experimental_option("prefs", prefs)

def main():
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)
    driver.get(login_url)
    time.sleep(2)

    username_field = driver.find_element(By.ID, "Username")
    password_field = driver.find_element(By.ID, "Password")

    username_field.send_keys(username)
    password_field.send_keys(password)

    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Log in']")))
    driver.execute_script("arguments[0].click();", login_button)

    time.sleep(5)

    with open("./filtered_pdf_links.txt", "r") as file:
        urls = file.readlines()

    for index, url in enumerate(urls):
        url = url.strip()
        driver.get(url)
        file_name = get_filename_from_url(url)
        wait_for_download_completion(download_directory, timeout=300)
        rename_downloaded_file(download_directory, file_name, f'{index}_{file_name}')
    driver.quit()

def is_download_in_progress(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.crdownload') or filename.endswith('.part'):
            return True
    return False

def wait_for_download_completion(directory, timeout=300):
    start_time = time.time()
    while is_download_in_progress(directory):
        time.sleep(10)
        if (time.time() - start_time) > timeout:
            raise Exception("Download did not complete within the allotted time.")
        print("Download in progress...")

def get_filename_from_url(url):
    parsed_url = urlparse(url)
    return os.path.basename(parsed_url.path)

def rename_downloaded_file(download_dir, old_filename, new_filename):
    old_file = os.path.join(download_dir, old_filename)
    new_file = os.path.join(download_dir, new_filename)
    while not os.path.exists(old_file):
        time.sleep(5)
    os.rename(old_file, new_file)

if __name__ == '__main__':
  main()