from item import Item
from sessionManager import SessionManager
from requests_html import HTMLSession


class PageScrapper:
    """
    Downloads page, simulating down scrolling and rendering js to show up all products
    
    Args: 
        url: page address with get parameters 
    
    self.result contains resulting list of products
    """

    def __init__(self, url):
        """Class is initialized with website address"""
        self.sessionManager = SessionManager()
        self.url = url
        self.rendered = True
        self.items = []
        self.result = []
    
    def get_page(self):
        """Downloads page, renders js, saves list of `items`"""
        r = self.sessionManager.request_page(self.url)
        if r is None:
            return

        items = r.html.find("div.J-offer-wrapper > div[data-content='productItem']")
        if len(items) == 0:
            items = r.html.find("div.item-content")
            self.rendered = False
        
        self.items = items


    def get_items(self):
        """Retrieves products from `items` list"""
        result = []
        for item in self.items:
            try:
                product = Item(item)

                if self.rendered:
                    product.get_item()
                else:
                    product.get_item_not_rendered()
                
                if product.valid:
                    obj = product.get_product()
                    result.append(obj)
            except:
                pass

        self.result = result
