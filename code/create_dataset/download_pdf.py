from selenium import webdriver
import time
from selenium.webdriver.common.by import By


# Replace these with your login credentials and the target URL
login_url = "https://www.nccn.org/login"  # URL of the login page
pdf_url = "https://nccn.org/professionals/physician_gls/pdf/prostate_harmonized-caribbean.pdf"  # URL of the PDF to download
username = "govindyadav.suny@gmail.com"
password = "_r$iGmySh%8j7iy"

# Set up the Selenium WebDriver
driver = webdriver.Chrome()

# Navigate to the login page and log in
driver.get(login_url)
time.sleep(2)  # Wait for the page to load

# Find the username, password fields and submit button
# These will need to be adjusted based on the website's HTML structure
username_field = driver.find_element(By.ID, "Username")
password_field = driver.find_element(By.ID, "Password")
login_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary")

# Input the username and password, then click the login button
username_field.send_keys(username)
password_field.send_keys(password)
login_button.click()
time.sleep(5)  # Wait for the login to complete

# Navigate to the PDF URL
driver.get(pdf_url)
time.sleep(5)  # Wait for the download to initiate and complete

# Close the browser
driver.quit()


# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # Replace these with your actual username and password
# username = "your_username"
# password = "your_password"

# # URL of the login page
# login_url = "https://www.nccn.org/login"

# # Setting up the WebDriver (assuming Chrome)
# driver = webdriver.Chrome(executable_path="path_to_your_chromedriver")

# try:
#     # Open the login page
#     driver.get(login_url)

#     # Wait for the username field to be present
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.ID, "ID_of_username_field"))
#     )

#     # Find and fill the username field
#     username_field = driver.find_element(By.ID, "ID_of_username_field")
#     username_field.send_keys(username)

#     # Find and fill the password field
#     password_field = driver.find_element(By.ID, "ID_of_password_field")
#     password_field.send_keys(password)

#     # Find and click the login button
#     login_button = driver.find_element(By.ID, "ID_of_login_button")
#     login_button.click()

#     # Wait for some element on the next page to ensure login success
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.SOME_IDENTIFIER, "some_value"))
#     )

# finally:
#     # Close the browser
#     driver.quit()
