import threading
import requests
from queue import Queue
from bs4 import BeautifulSoup
import logging


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def scrape_url(url, lock):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        title = soup.title.string.strip() if soup.title else "No title"
        with lock:
            logging.info(f"Title: {title}")

        paragraphs = soup.find_all("p")
        for paragraph in paragraphs:
            with lock:
                logging.info(paragraph.text.strip())
    except requests.RequestException as e:
        with lock:
            logging.error(f"Request error scraping {url}: {e}")
    except Exception as e:
        with lock:
            logging.error(f"Error scraping {url}: {e}")


def worker(queue, lock):
    while True:
        url = queue.get()
        if url is None:
            break
        scrape_url(url, lock)
        queue.task_done()


num_threads = 4


queue = Queue()


urls = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3",
]


for url in urls:
    queue.put(url)


lock = threading.Lock()


threads = []
for _ in range(num_threads):
    t = threading.Thread(target=worker, args=(queue, lock), daemon=True)
    t.start()
    threads.append(t)


queue.join()


for _ in range(num_threads):
    queue.put(None)
for t in threads:
    t.join()

logging.info("Scraping completed.")
