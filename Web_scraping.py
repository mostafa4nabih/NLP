import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote, urlparse, parse_qs


def google_search(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        response = requests.get(f"https://www.google.com/search?q={query}", headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.text
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return ""


def extract_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    for item in soup.find_all('a', href=True):
        link = item['href']
        if link and "s&q=&rct" in link:
            clean_link = link.split("U&url=")[1]
            links.append(clean_link)
    return links


def extract_text_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = ' '.join([p.text for p in soup.find_all('p')])
        return text
    except requests.RequestException as e:
        print(f"Failed to retrieve {url}: {e}")
        return ""


def main(search_query):
    html = google_search(search_query)
    if not html:
        print("Failed to get any HTML from Google.")
        return
    urls = extract_links(html)
    print(urls)
    if not urls:
        print("No URLs found in the search results.")
        return

    filename = f"{search_query}_webscraper.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        for url in urls:  # Limit to the first 5 results
            print("URL:", url)
            text = extract_text_from_url(url)
            if text:
                file.write(text + '\n')  # Write each text on a new line
                print("Extracted Text:", text[:500])  # Show first 500 characters of the extracted text
            else:
                print("Failed to extract text from URL.")

        else:
            print("Failed to extract text from URL.")


if __name__ == "__main__":
    search_query = "الله اكبر"
    main(search_query)  # Modify the search query as needed
