import sys
import json
from urllib import parse
import warnings
import itertools
from sessionManager import SessionManager
from pageScrapper import PageScrapper

warnings.filterwarnings('ignore')


def main():
    search_url = "https://russian.alibaba.com/trade/search?fsb=y&IndexArea=product_en&SearchText="

    # Retrieve command line args
    pages = sys.argv[1].rstrip()
    search_str = ""
    if pages.isdigit():
        pages = int(pages)
        search_str = sys.argv[2].rstrip()
    else: 
        pages = 2
        search_str = sys.argv[1].rstrip()

    merged_result = []
    sessionManager = SessionManager()

    search_url = search_url + parse.quote_plus(search_str) + '&page='
    # Iterate over pages
    # try-except is used to hide any errors and pass only valid json to output
    for i in range(1, pages + 1):
        url = search_url + str(i)
        scrapper = PageScrapper(url)
        scrapper.sessionManager = sessionManager
        try:
            scrapper.get_page()
            scrapper.get_items()
            merged_result.append(scrapper.result)
        except:
            pass
    
    del sessionManager

    merged_result = [i for i in itertools.chain(*merged_result)]
    print(json.dumps(merged_result, indent=4, sort_keys=True, ensure_ascii=False))

if __name__ == '__main__':
    main()