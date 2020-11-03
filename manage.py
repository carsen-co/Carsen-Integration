import os, sqlite3, threading
from time import sleep

from db import DB
from crawler import CRAWLER
from mobile_de import scraper

def process_listings_links(db):
    sleep(5)
    while True:
        urls = db.read_table("listings_links")
        for url in urls:
            car_data, db_name = scraper.get_car_data(url + "&lang=en", find_db=True)
            db.add_value(db_name, car_data)
        sleep(5)


if __name__ == "__main__":
    db = DB()

    search_thread = threading.Thread(target=process_listings_links, args=(db,))
    search_thread.start()

    CR = CRAWLER(db)

    input()
    while CR.running:
        sleep(5)

    CR.stop()
    search_thread.join()
    os._exit(0)
