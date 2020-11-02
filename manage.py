import os
from time import sleep
from threading import Thread
import db, crawler, mobile_de

def process_listings_links():
    sleep(5)
    while True:
        try:
            url = crawler.listing()
            print(url)
            car_data, db_name = mobile_de.get_car_data(url, find_db=True)
            print(db_name, car_data[1:])
            db.add_value(db_name, car_data)
        except Exception as e:
            sleep(5)
            print(e)

if __name__ == "__main__":
    database = db.DB()

    search_thread = Thread(target=process_listings_links, args=())
    search_thread.start()

    try:
        crawler = crawler.CRAWLER(database)

    except KeyboardInterrupt:
        crawler.stop()
        search_thread.join()
        os._exit(0)
