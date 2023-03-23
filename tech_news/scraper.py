import time

import requests
from parsel import Selector

from tech_news.database import create_news


# Requisito 1
def fetch(url):
    try:
        time.sleep(1)
        response = requests.get(url, timeout=3)
        response.status_code

        if response.status_code == 200:
            return response.text
        else:
            return None

    except requests.Timeout:
        return None


# Requisito 2
def scrape_noticia(html_content):
    selector = Selector(html_content)
    result = {}
    result["url"] = selector.css("link[rel=canonical]::attr(href)").get()
    result["title"] = selector.css(".tec--article__header__title::text").get()
    result["timestamp"] = selector.css("time::attr(datetime)").get()
    result["writer"] = (
        selector.css(".tec--author__info__link::text").get().strip()
        if selector.css(".tec--author__info__link::text").get()
        else None
    )
    shares_verify = selector.css(".tec--toolbar__item::text").get()
    if shares_verify:
        shares = int(shares_verify.split()[0])
    else:
        shares = 0
    result["shares_count"] = shares
    comments_verify = selector.css("#js-comments-btn::attr(data-count)").get()
    if comments_verify:
        comments = int(comments_verify)
    else:
        comments = 0
    result["comments_count"] = comments
    result["summary"] = "".join(
        selector.css(".tec--article__body > p:first-child *::text").getall()
    )
    sources = selector.css(".z--mb-16 div a.tec--badge::text").getall()
    source_list = []
    for source in sources:
        source_list.append(source.strip())
    result["sources"] = source_list
    categories = selector.css("#js-categories a.tec--badge::text").getall()
    category_list = []
    for category in categories:
        category_list.append(category.strip())
    result["categories"] = category_list
    return result


# Requisito 3
def scrape_novidades(html_content):
    selector = Selector(text=html_content)
    list = selector.css("h3 a.tec--card__title__link::attr(href)").getall()
    return list


# Requisito 4
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    next = selector.css(".tec--btn::attr(href)").get()
    return next


# Requisito 5
def get_tech_news(amount):
    URL = "https://www.tecmundo.com.br/novidades"
    links = []
    result = []

    while len(links) < amount:
        content = fetch(URL)
        links.extend(scrape_novidades(content))
        URL = scrape_next_page_link(content)
    for news in links[:amount]:
        result.append(scrape_noticia(fetch(news)))

    create_news(result)
    return result
