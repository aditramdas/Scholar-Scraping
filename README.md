# Scholar-Scraping

This is a scraping project, using Selenium, used to scrape through the publications of a particular person, wherein for each publication the research paper is downloaded, and the details pertaining to the paper is stored in a csv sheet. 

The same process is done for the co-authors of the main author. Separate CSVs are maintained for each author.

# Why Selenium instead of BeautifulSoup?
The Google Scholar website kept blocking the scraping script when used with BeautifulSoup.

# Folder Structure
 * selenium.py
 * CSVs
   * author1.csv
   * author2.csv
 * Downloads
   * paper1.pdf
   * paper2.pdf

