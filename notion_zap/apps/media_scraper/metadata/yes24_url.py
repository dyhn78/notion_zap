from urllib import parse

import requests
from bs4 import BeautifulSoup


def scrap_yes24_url(book_name) -> str:
    book_name = ''.join(filter(lambda x: str.isalnum(x) or x == ' ', book_name))
    book_name_encoded = parse.quote_plus(book_name, encoding='euc-kr')
    url_main_page = 'http://www.yes24.com'
    url = f"http://www.yes24.com/searchcorner/Search?keywordAd=&keyword=&domain=BOOK&" \
          f"qdomain=%c5%eb%c7%d5%b0%cb%bb%f6&query={book_name_encoded}"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html5lib')

    tag_book = '#yesSchList > li:nth-child(1) > div > ' \
               'div.item_info > div.info_row.info_name > a.gd_name'
    book = soup.select_one(tag_book)

    try:
        url_part = book.attrs['href']
        if 'yes24' not in url_part:
            url = url_main_page + url_part
        else:
            url = url_part
    except (ValueError, AttributeError):
        return ''
    if '?OzSrank=1' in url:
        url = url[0:-len('?OzSrank=1')]
    return url
