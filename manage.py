import os, sqlite3, threading
from time import sleep

from db import DB
from crawler import CRAWLER
from mobile_de import scraper


def process_listings_links(db, cr):
    sleep(5)
    while True:
        urls = cr.listings_links
        for url in urls:
            car_data, db_name = scraper.get_car_data(url + "&lang=en", find_db=True)
            db.add_value(db_name, car_data)
            cr.listings_links.remove(url)
            if not cr.running:
                break
        if not cr.running:
            break
        sleep(5)


if __name__ == "__main__":
    database = DB()
    crawlr = CRAWLER(database)

    search_thread = threading.Thread(
        target=process_listings_links,
        args=(
            database,
            crawlr,
        ),
    )
    search_thread.start()

    try:
        input("Type anything to stop execution: ")
    except KeyboardInterrupt:
        pass
    finally:
        print("Interruption detected, stopping execution")
        crawlr.stop()
        print("Crawler stopped")
        search_thread.join()
        print("Search thread stopped")
        database.close_conn()
        print("Database closed")
        os._exit(0)
