from requests_html import HTMLSession

class SessionManager(object):
    """
    Manages HTMLSession to close everything when needed
    """
    def __init__ (self):
        self.session = HTMLSession()

    def request_page(self, url):
        """Gets page, renderes it, closes session"""
        r = self.session.get(url)
        try:
            r.html.render(timeout=30, scrolldown=True)
            r.close()
            if "It’s currently a bit busy" in r.html.text:
                return None
            return r
        except:
            r.close()
        
    def __del__(self):
        self.session.close()


