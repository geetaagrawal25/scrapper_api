# File used to build dataset

from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv

executable_path = {"executable_path": "/chromedriver.exe"}
browser = Browser("chrome", **executable_path, headless=False)

def get_truths():
    fh_1 = open('truths.csv', 'w')
    writer = csv.writer(fh_1)
    writer.writerow(["name", "text", "category"])

    browser.visit("https://www.politifact.com/factchecks/list/?ruling=true")

    for i in range(2, 10000):        
        try:
            soup = BeautifulSoup(browser.html, "html.parser")
            page_names = soup.find_all("a", class_="m-statement__name")
            page_texts = soup.find_all("div", class_="m-statement__quote")

            names = [i.text.strip() for i in page_names]
            texts = [i.text.strip() for i in page_texts]

            df = pd.DataFrame({
                "name": names,
                "text": texts,
                "category": "true",
            })

            for index, row in df.iterrows():
                writer.writerow(row)
        
            browser.visit(f"https://www.politifact.com/factchecks/list/?page={i}&ruling=true")
        except:
            break


def get_falses():
    fh = open('falses.csv', 'w')
    writer_2 = csv.writer(fh)
    writer_2.writerow(["name", "text", "category"])

    browser.visit("https://www.politifact.com/factchecks/list/?ruling=false")

    for i in range(2, 10000):
        try:
            soup = BeautifulSoup(browser.html, "html.parser")
            page_names = soup.find_all("a", class_="m-statement__name")
            page_texts = soup.find_all("div", class_="m-statement__quote")

            names = [i.text.strip() for i in page_names]
            texts = [i.text.strip() for i in page_texts]

            df = pd.DataFrame({
                "name": names,
                "text": texts,
                "category": "false",
            })

            for index, row in df.iterrows():
                writer_2.writerow(row)
        
            browser.visit(f"https://www.politifact.com/factchecks/list/?page={i}&ruling=false")
        except:
            break

    fh.close()


def main():
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures_list = [
            executor.submit(get_truths),
            executor.submit(get_falses),
        ]

        for future in as_completed(futures_list):
            future.result()


if __name__ == "__main__":
    main()