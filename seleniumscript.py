from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import os
import time
from urllib.parse import urlparse
import shutil

download_dir = "E:\\Projects\\ScrapingScholar\\Downloads"

service = Service(ChromeDriverManager().install())

chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True,
    "plugins.always_open_pdf_externally": True
}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
driver = webdriver.Chrome(service=service, options=chrome_options)

def get_article_details(driver, article_url, author_name):
    try:
        driver.get(article_url)
        wait = WebDriverWait(driver, 4)
    except:
        return {
            'Title': "Not found",
            'Authors': "Not found",
            'Publisher': "Not found",
            'Description': "Not found",
            'PDF Link': ""
        }

    try:
        title = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'gsc_oci_title_link'))).text
    except:
        title = "Not found"

    try:
        authors_list = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'gsc_oci_value'))).text
    except:
        authors_list = "Not found"

    try:
        publisher_info = wait.until(EC.presence_of_element_located((By.XPATH, '//div[text()="Publisher"]/following-sibling::div'))).text
    except:
        publisher_info = "Not found"

    try:
        pdf_link = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.gsc_oci_title_link'))).get_attribute('href')
    except:
        pdf_link = ""
    try:
        pdf_link = driver.find_element(By.CSS_SELECTOR, 'div.gsc_oci_title_ggi > a')
        pdf_url = pdf_link.get_attribute('href')
        # driver.get(pdf_url)
        parsed_url = urlparse(pdf_url)
        path = parsed_url.path
        file_name = path.split('/')[-1]
        # wait_for_downloads(download_dir, file_name)
        # move_file_to_author_dir(download_dir, author_name, file_name)
        
    except:
        file_name = ""
    try:
        description = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'gsh_csp'))).text
    except:
        description = "Not found"

    return {
        'Title': title,
        'Authors': authors_list,
        'Publisher': publisher_info,
        'Description': description,
        'PDF Link': file_name
    }
def move_file_to_author_dir(download_dir, author_name, file_pattern):
    """
    Move the downloaded file (matching file_pattern) to a directory named after the author.
    """
    author_dir = os.path.join(download_dir, author_name.replace(" ", "_").replace("/", "_"))
    if not os.path.exists(author_dir):
        os.makedirs(author_dir)
    
    for filename in os.listdir(download_dir):
        if file_pattern in filename:
            shutil.move(os.path.join(download_dir, filename), author_dir)
            print(f"Moved {filename} to {author_dir}")
            break
    else:
        print(f"No file matching {file_pattern} found to move.")
def wait_for_downloads(download_dir, file_pattern, timeout=300):
    """
    Wait until the specific file is downloaded by checking for its presence
    and ensuring no temporary download files (.crdownload for Chrome) remain.
    """
    end_time = time.time() + timeout
    found = False
    while True:
        for filename in os.listdir(download_dir):
            if file_pattern in filename and not filename.endswith('.crdownload'):
                found = True
                break
        if found:
            break
        time.sleep(1)  # Check every second
        if time.time() > end_time:
            raise Exception("Download timed out waiting for specific file.")
        
def scrape_google_scholar_profile(url):
    driver.get(url)
    author_name = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "gsc_prf_in"))
).text  
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@class='gsc_a_at']")))
    article_links = [elem.get_attribute('href') for elem in driver.find_elements(By.XPATH, "//a[@class='gsc_a_at']")]

    # Create or open a CSV file named after the author
   
    csv_filename = f"{author_name.replace(' ', '_')}_articles.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8') as file:
        headers = ['Title', 'Authors', 'Publisher', 'Description', 'PDF Link']
        csv_writer = csv.DictWriter(file, fieldnames=headers)
        csv_writer.writeheader()

        for link in article_links:
            details = get_article_details(driver, link,author_name)
            csv_writer.writerow(details)

def get_coauthors(prof_url):
    driver.get(prof_url)
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".gsc_rsb_aa .gsc_rsb_a_desc a")))
    coauthor_elements = driver.find_elements(By.CSS_SELECTOR, ".gsc_rsb_aa .gsc_rsb_a_desc a")
    coauthor_urls = [element.get_attribute('href') for element in coauthor_elements]
    return coauthor_urls

def main():
    profile_url = 'https://scholar.google.com/citations?user=jD_jKZQAAAAJ&hl=en'
    scrape_google_scholar_profile(profile_url)

    coauthors_urls = get_coauthors(profile_url)
    for coauthor_url in coauthors_urls:
        # Fetch the co-author's name from their profile URL or page (this part is left for implementation)
        # For demonstration, let's just use a placeholder name extracted from the URL or another method
        
         
        scrape_google_scholar_profile(coauthor_url)

    driver.quit()

if __name__ == "__main__":
    main()
