from requests_html import HTMLSession
import sys

class SessionManager(object):
    """
    Manages HTMLSession to close everything when needed
    """
    def __init__ (self):
        self.session = HTMLSession()

    def __restart_session(self):
        self.session.close()
        self.session = HTMLSession()

    def __request_page(self, url):
        """Gets page, renderes it, closes session"""
        r = self.session.get(url)
        try:
            r.html.render(timeout=30, scrolldown=True)
            if "It’s currently a bit busy" in r.html.text:
                raise ValueError("\'It’s currently a bit busy\" page is shown")
            r.close()
            return r
        except Exception as err:
            r.close()
            raise err
        
    def request_page(self, url):
        """Gets page, renderes it, closes session"""
        attempts = 3
        for i in range(0, attempts):
            try:
                response = self.__request_page(url)
                return response
            except Exception as err:
                # if last iteration
                if i == attempts - 1:
                    print('Couldn\'t get {} after {} attempts'.format(url, attempts), file=sys.stderr)
                    print(err, file=sys.stderr)
                else:
                    self.__restart_session()

    def __del__(self):
        self.session.close()


