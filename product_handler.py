import re
from typing import Optional

from playwright.sync_api import BrowserContext

from product import Product
from user_pool import UserPool

kart_url = "https://www.matas.dk/indkoebskurv"
checkout_url = "https://www.matas.dk/levering"

brand_path = "//h1/preceding-sibling::div[1]/a"
name_path = "//h1"

currency_mapper = {"kr": "DKK"}


class ProductHandler:
    def __init__(self, product_url: str, context: BrowserContext):
        self.product_url = product_url
        self.context = context
        self.product = None

        self.process()

    def get_product(self) -> Optional[Product]:
        return self.product

    def process(self):
        print("Url to process: {}".format(self.product_url))

        self.get_basic_metadata()
        self.get_shipping_suppliers()

    def get_basic_metadata(self):
        page = self.context.new_page()
        page.goto(self.product_url)

        name = page.locator(name_path).text_content()
        brand = page.locator(brand_path).text_content()

        # Regex field
        spans = page.locator("//span")
        pattern = re.compile(r"^\d+,\d+ kr.$")
        matches = []
        for i in range(spans.count()):
            data = spans.nth(i).text_content()
            if pattern.search(data):
                matches.append(data)

        if len(matches) > 1:
            print("Multiple matches found for field: price")

        # Locale currency format can be a problem for , . and currency
        price_data = matches[0].strip(".")
        price, currency = price_data.split(" ")
        price = price.replace(",", ".")
        currency = currency_mapper[currency]

        self.product = Product(
            brand=brand,
            name=name,
            price=price,
            currency=currency,
            url=self.product_url,
            shipping_suppliers=[],
        )

    def clean_shipping_suppliers(self, data: str) -> list[str]:
        entries = re.split(",| ", data)

        # We could use NLTK for stemming here
        common_words = ["", "eller"]
        suppliers = [e for e in entries if e not in common_words]

        return suppliers

    def get_shipping_suppliers(self) -> list[str]:
        page = self.context.new_page()
        page.goto(self.product_url)

        page.click("//button[contains(., 'Acceptér alle')]")

        page.click("//button[text()='Læg i kurv']")
        page.wait_for_load_state("networkidle")

        page.goto(checkout_url)

        page.wait_for_load_state("networkidle")

        pool = UserPool()

        # Get a single random user
        user = pool.random_user()
        print("Using user: {}".format(user))

        page.locator("[name='name']").press_sequentially(user.name, delay=100)
        page.locator("[name='address']").press_sequentially(user.address, delay=100)
        page.locator("[name='zipCode']").press_sequentially(user.zipCode, delay=100)
        page.locator("[name='mobile']").press_sequentially(user.mobile, delay=100)
        page.locator("[name='email']").press_sequentially(user.email, delay=100)

        page.click("//button[contains(., 'Fortsæt til levering')]")

        page.wait_for_selector("//button[text()='Se flere leveringsmuligheder']")

        page.click("//button[text()='Se flere leveringsmuligheder']")

        # page.screenshot(full_page=True, path=f"kart.png")

        suppliers_raw = page.locator("//div[contains(@class, 'ShippingSuppliers')]")
        suppliers = set()

        count = suppliers_raw.count()
        for i in range(count):
            s = self.clean_shipping_suppliers(suppliers_raw.nth(i).text_content())
            suppliers.update(s)
        print(suppliers)

        self.product.shipping_suppliers = " ".join(suppliers)

        return list(suppliers)
