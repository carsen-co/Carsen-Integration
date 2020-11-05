import os, sqlite3, threading
from time import sleep

from database import DB
from crawler import CRAWLER
from mobile_de import scraper
from settings import DB_NAME


def process_listings_links(db, cr):
    sleep(5)
    while True:
        urls = cr.listings_links
        for url in urls:
            cr.listings_links.remove(url)
            cr.processed_links.append(url)
            try:
                try:
                    car_data, db_name = scraper.get_data(url, find_db=True)
                except TypeError:
                    # data is None
                    continue
            except Exception as e:
                continue
            db.add_value(db_name, car_data)
            if not cr.running:
                break
        if not cr.running:
            break
        sleep(5)


def status(cr, db):
    print("\n" * 5, end="")
    while True:
        print("\033[F" * 6)
        print(
            f"Execution Stats",
            f"       Active: {len(cr.active_links)}",
            f"     Listings: {len(cr.listings_links)}",
            f"    Processed: {len(cr.processed_links)}",
            f"Database size: {os.stat(DB_NAME).st_size / (1024**2):.3f}MB",
            # f"      Indexed: {db.read_all()}",
            sep="\n",
        )
        sleep(1)
        if cr.running == False:
            break


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

    status_thread = threading.Thread(
        target=status,
        args=(crawlr, database),
    )
    status_thread.start()

    try:
        input()
    except KeyboardInterrupt:
        pass
    finally:
        crawlr.stop(database)
        search_thread.join()
        database.close_conn()
        status_thread.join()
        # os._exit(0)
