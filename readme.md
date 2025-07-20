JNTUH R18 Results Scraper
A Python script to automatically scrape the latest "(R18)" regulation examination results from the JNTUH results website.

Description
This script navigates to the JNTUH results homepage, parses the HTML, and extracts the links and descriptions for all currently listed results that belong to the R18 regulation. It's a useful tool for quickly finding specific result notifications without manually checking the website.

Features
Fetches the most up-to-date list of results directly from the JNTUH website.

Filters specifically for results containing the "(R18)" tag.

Handles common web scraping issues, such as User-Agent blocking and connection errors.

Robust parser handling: tries to use the fast lxml parser and falls back to the standard html.parser if lxml is not installed.

Constructs full, clickable URLs from the site's relative links.

Installation
Clone or download the repository/script.

Install the required Python libraries. You will need requests and beautifulsoup4. The lxml library is optional but highly recommended for better performance.

Open your terminal or command prompt and run:

pip install requests beautifulsoup4 lxml

Usage
To run the script, navigate to the directory where you saved the file in your terminal and execute it with Python:

python your_script_name.py

Example Output:
Attempting to fetch data from: http://results.jntuh.ac.in/jsp/home.jsp

--- Found R18 Results ---

Name: B.Tech IV Year II Semester (R18) Regular Examinations Results June-2025
Link: http://results.jntuh.ac.in/jsp/SearchResult.jsp?degree=btech&examCode=1862&etype=r17&type=intgrade
------------------------------------------------------------

Full Script
<details>
<summary>Click to view the complete Python code</summary>

import requests
from bs4 import BeautifulSoup
# In older versions of BeautifulSoup, FeatureNotFound is in the main bs4 package.
# This import is more compatible across different versions.
from bs4 import FeatureNotFound

# Step 1: Target the correct URL where the results table is located.
url = "http://results.jntuh.ac.in/jsp/home.jsp"

# This is the base URL that will be prepended to the relative href links.
base_url = "http://results.jntuh.ac.in"

# Add a User-Agent header to mimic a real browser.
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Connection': 'keep-alive' # Explicitly ask to keep the connection open
}

print(f"Attempting to fetch data from: {url}")

try:
    # Use a Session object to persist parameters and handle connections more robustly.
    with requests.Session() as s:
        s.headers.update(headers)
        
        # Step 2: Send the request using the session object.
        # A timeout is good practice.
        response = s.get(url, timeout=15)
    
    # Raise an exception if the request was not successful (e.g., 404, 500 errors)
    response.raise_for_status()

    # Step 3: Parse the HTML content of the page.
    # We try to use the 'lxml' parser first because it's faster.
    # If it's not installed, a FeatureNotFound error is raised, and we fall back
    # to the built-in 'html.parser'.
    try:
        soup = BeautifulSoup(response.content, 'lxml')
    except FeatureNotFound:
        print("lxml not found, falling back to html.parser.")
        soup = BeautifulSoup(response.content, 'html.parser')

    # Step 4: Find all <a> tags that have a <p> tag inside.
    # This logic correctly identifies the target elements based on your HTML snippet.
    results = []
    
    # We search for all 'a' tags that have an 'href' attribute.
    for a_tag in soup.find_all('a', href=True):
        p_tag = a_tag.find('p')
        # Check if a <p> tag exists within the <a> tag.
        if p_tag:
            # Get the text from the <p> tag, stripping any extra whitespace.
            name = p_tag.get_text(strip=True)
            
            # **FILTERING LOGIC**: Check if 'r18' (case-insensitive) is in the result's name.
            if '(r18)' in name.lower():
                # The href attribute is relative (e.g., '/jsp/SearchResult.jsp...').
                # We need to join it with the base_url to create a full, clickable URL.
                relative_link = a_tag['href']
                full_link = base_url + relative_link
                
                results.append((full_link, name))

    # Step 5: Output the filtered data.
    if results:
        print("\n--- Found R18 Results ---\n")
        for link, name in results:
            print("Name:", name)
            print("Link:", link)
            print('-' * 60)
    else:
        print("\nCould not find any 'R18' results matching the criteria.")
        print("The website's structure may have changed or no R18 results are listed.")

except requests.exceptions.RequestException as e:
    print(f"An error occurred while fetching the URL: {e}")

</details>

How the Code Works
The script follows a clear, step-by-step process to extract the information.

1. Setup and Configuration
Imports: Loads the necessary libraries (requests, BeautifulSoup).

URLs: Defines the target URL for the results page and a base_url to construct full links.

Headers: Sets a User-Agent header to mimic a real browser, preventing the server from blocking the script.

2. Fetching the Webpage
A requests.Session object is used to manage the connection.

It sends an HTTP GET request to the target URL.

Includes error handling (try...except) to catch network issues and checks for bad HTTP responses (like 404 Not Found).

3. Parsing the HTML
The downloaded HTML content is passed to BeautifulSoup.

The script creates a soup object, which is a structured representation of the HTML, making it easily searchable.

4. Finding and Filtering Data
The script uses soup.find_all('a', href=True) to get a list of all link tags on the page.

It then loops through each link:

It finds the nested <p> tag inside the link.

It extracts the text from the <p> tag (e.g., "B.Tech IV Year...").

Crucially, it converts the text to lowercase and checks if '(r18)' is present.

If the text matches, it constructs the full URL and saves the link and its description.

5. Displaying Results
Finally, the script prints all the filtered results it found in a clean, readable format. If no R18 results are listed on the page, it prints a notification message.