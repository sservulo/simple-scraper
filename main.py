import sys

from playwright.sync_api import sync_playwright
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from product import ProductORM
from product_handler import ProductHandler

# Database configs
user = "root"
password = "password"
host = "127.0.0.1"
port = 3306
database = "scraper"


url = "https://www.matas.dk/urban-decay-all-nighter-vitamin-c-setting-spray-118-ml"


def get_connection():
    return create_engine(
        url="mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database
        ),
        echo=True,
    )


if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]

    engine = get_connection()
    ProductORM.metadata.create_all(engine)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        handler = ProductHandler(url, context)

        product = handler.get_product()

        print("Product: {}".format(product))

        product_orm = ProductORM.from_dataclass(product)
        with Session(engine) as session:
            session.add(product_orm)
            session.commit()
