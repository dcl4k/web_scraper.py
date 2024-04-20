import collections
import requests
from bs4 import BeautifulSoup


def get_html_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.text
    except requests.RequestException as e:
        # Handle exceptions that may occur during the request
        #print(f"Failed to retrieve content from {url}: {str(e)}")
        return None


def get_links_on_page(base_url, html):
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a')  # Finds all <a> tags
    urls = []
    for link in links:
        href = link.get('href')
        if href:
            # Check if the URL is relative and convert it to absolute
            if href.startswith('/'):
                href = requests.compat.urljoin(base_url, href)
            urls.append(href)
    return urls



class WCrawler:

    def __init__(self, url):  # constructor method
        self.visited_urls = set()  # create the visited_urls list for processed urls
        self.url_queue = collections.deque()  # create the queue to be processed
        self.url_queue.appendleft(url)  # add the provided urls to the deque

    def get_url(self, url):
        html = get_html_content(url)
        if html is None:
            #print(f"Skipping {url}, as no HTML content could be retrieved.")
            return

        links = get_links_on_page(url, html)
        for link in links:
            if link not in self.visited_urls:
                self.visited_urls.add(link)
                self.url_queue.appendleft(link)

    def execute(self):
        while self.url_queue:
            current_url = self.url_queue.pop()
            self.get_url(current_url)
        return list(self.visited_urls)


if __name__ == '__main__':
    initial_url = 'http://books.toscrape.com'  # Set the URL you want to start crawling from
    crawler = WCrawler(initial_url)
    visited = crawler.execute()
    print("Visited URLs:")
    for url in visited:
        print(url)