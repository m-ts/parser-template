import requests_html
from typing import List
import re

class Item:
    """
    Retrieves products from html with selectors

    Args:
        item_el: one item element

    Get result with `get_product()`
    """

    def __init__(self, item_el: List[requests_html.Element]):
        """Class is initialized with item"""
        self.item_el = item_el

        self.image_url = ""
        self.description = ""
        self.priceFrom = 0.0
        self.priceTo = 0.0
        self.minOrder = 0
        self.currency = ""
        self.valid = False

    def get_currency(self, str, exact):
        curr = ""
        if exact:
            curr_index = str[::-1].find('\xa0')
            curr = str[-curr_index:]
            if '/' in str:
                curr_index = curr.find(' ')
                curr = curr[:curr_index]
        else:
            curr = (re.findall(r'[^0-9,-\xa0]+[-]', str)[0])[:-1]

        return curr

    def get_item(self):
        """Retrieves values from item when page is rendered correctly"""
        image_url = self.get_element("div[flasher-type='mainImage']") # gives NoneType for promotion card (1 per page)
        image_url = "https:" + image_url.attrs["data-image"]

        name = self.get_element("h4.organic-gallery-title__outter").attrs["title"]

        price_str = self.get_element("p.gallery-offer-price").text
        price = re.findall(r'[0-9]+[,.][0-9]+', price_str)
        curr = ""
        if len(price) == 1: # exact price
            low = price[0]
            high = price[0]
        else:
            low = price[0]
            high = price[1]
        curr = self.get_currency(price_str, len(price)==1)

        min_order = self.get_element("p.gallery-offer-minorder")
        if min_order is None:
            min_order = "1"
        else:
            min_order = re.findall(r'[0-9]+', min_order.text)[0]

        self.image_url = image_url
        self.description = name
        self.priceFrom = float(low.replace(',', '.'))
        self.priceTo = float(high.replace(',', '.'))
        self.minOrder = int(min_order)
        self.currency = curr
        self.valid = True

    def get_item_not_rendered(self):
        """Retrieves values from item when page is NOT rendered correctly"""
        image_url = self.get_element("div.img-wrap > a > img") # gives NoneType for promotion card (1 per page)
        image_url = "https:" + image_url.attrs["src"]

        name = self.get_element("h2.title > a").text

        price_str = self.get_element("div.price").text
        price = re.findall(r'[0-9]+[,.][0-9]+', price_str)
        curr = ""
        if len(price) == 1: # exact price
            low = price[0]
            high = price[0]
        else:
            low = price[0]
            high = price[1]

        curr = self.get_currency(price_str, len(price)==1)

        min_order = self.get_element("div.min-order")
        if min_order is None:
            min_order = "1"
        else:
            min_order = re.findall(r'[0-9]+', min_order.text)[0]

        self.image_url = image_url
        self.description = name
        self.priceFrom = float(low.replace(',', '.'))
        self.priceTo = float(high.replace(',', '.'))
        self.minOrder = int(min_order)
        self.currency = curr
        self.valid = True

    def get_element(self, selector) -> requests_html.Element:
        return self.item_el.find(selector, first=True)

    def get_product(self):
        """Returnes product characteristics inside dictionary"""
        obj = {}
        obj["imageUrl"] = self.image_url
        obj["description"] = self.description
        obj["priceFrom"] = self.priceFrom
        obj["priceTo"] = self.priceTo
        obj["minOrder"] = self.minOrder
        obj["curr"] = self.currency
        return obj
