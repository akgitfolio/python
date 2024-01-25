import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


def get_category_url(base_url, category_name):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, "html.parser")
    category_links = soup.find_all("a", href=True)
    for link in category_links:
        if category_name.lower() in link.text.lower():
            return base_url + link["href"]
    return None


def scrape_books_from_category(category_url):
    books = []
    page_number = 1
    while True:
        url = category_url.replace("index.html", f"page-{page_number}.html")
        response = requests.get(url)
        if response.status_code != 200:
            break
        soup = BeautifulSoup(response.content, "html.parser")
        book_items = soup.find_all("article", class_="product_pod")
        for item in book_items:
            title = item.h3.a["title"]
            price = item.find("p", class_="price_color").text
            availability = item.find("p", class_="instock availability").text.strip()
            books.append({"Title": title, "Price": price, "Availability": availability})
        page_number += 1
        time.sleep(1)
    return books


def save_to_csv(books, filename):
    df = pd.DataFrame(books)
    df.to_csv(filename, index=False)


def main():
    base_url = "http://books.toscrape.com/"
    category_name = input(
        "Enter the category you want to scrape (e.g., Travel, Science Fiction): "
    )
    category_url = get_category_url(base_url, category_name)
    if category_url:
        print(f"Scraping books from category: {category_name}")
        books = scrape_books_from_category(category_url)
        if books:
            save_to_csv(books, f"{category_name}_books.csv")
            print(f"Data saved to {category_name}_books.csv")
        else:
            print("No books found in this category.")
    else:
        print("Category not found.")


if __name__ == "__main__":
    main()
