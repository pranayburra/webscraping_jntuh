import requests
from bs4 import BeautifulSoup

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

