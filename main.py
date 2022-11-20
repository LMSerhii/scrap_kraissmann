import json

import requests

from bs4 import BeautifulSoup


def get_data():
    """ """
    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    all_data = {}
    total_items_count = 0
    total_images_count = 0
    category_items = []
    with requests.Session() as session:

        urls = [
            "https://kraissmann.com/akumulyatorni-instrumenti/",
            "https://kraissmann.com/sadovij-instrument-ta-obladnannya/",
            "https://kraissmann.com/vidrizannya-shlifuvannya-frezeruvannya/",
            "https://kraissmann.com/sverdlinnya-zagvinchuvannya-dovbannya-zmishuvannya/",
            "https://kraissmann.com/pili/",
            "https://kraissmann.com/stacionarni-mashini/",
            "https://kraissmann.com/ochishuvalne-obladnannya/",
            "https://kraissmann.com/pidjomne-obladnannya/",
            "https://kraissmann.com/vimiryuvalna-tehnika/",
            "https://kraissmann.com/pobutove-obladnannya/",
            "https://kraissmann.com/vsmoktuvannya-ta-vidalennya-pilu/",
            "https://kraissmann.com/budivelnij-instrument/"
        ]

        for url in urls:

            category = {}

            response = session.get(url=url, headers=headers)

            soup = BeautifulSoup(response.text, "lxml")
            subcategories = soup.find_all("div", class_="col-sm-3 catimg")

            category_name_translit = url.split("/")[-2]
            category['category_name_translit'] = category_name_translit

            subcategory_items = []
            for subcategory in subcategories:

                subcategory_dict = {}

                subcategory_link = subcategory.select_one('a').get('href')
                subcategory_name_translit = subcategory_link.split("/")[-2]
                subcategory_dict['subcategory_name'] = subcategory_name_translit

                subcategory_link_to_image = subcategory.select_one("a img").get("src")
                subcategory_dict['subcategory_link_to_image'] = subcategory_link_to_image

                response = session.get(url=subcategory_link, headers=headers)
                soup = BeautifulSoup(response.text, 'lxml')
                products = soup.find_all("div", class_="product-thumb")
                total_items_count += len(products)

                cards = []
                for index, product in enumerate(products):

                    product_link = product.select_one("div.caption").select_one("h4 a").get('href')

                    response = session.get(url=product_link, headers=headers)
                    soup = BeautifulSoup(response.text, 'lxml')

                    card = {}

                    product_name_translit = product_link.split("/")[-1]
                    card['product_name_translit'] = product_name_translit

                    specification_html = soup.find("div", id="tab-specification")
                    card['specification_html'] = str(specification_html)

                    description_html = soup.find("div", id="tab-description")
                    card['description_html'] = str(description_html)

                    images_links_search = soup.find("ul", class_="thumbnails").find_all("li")
                    product_image_links = [link.find("a").get('href') for link in images_links_search]
                    card['product_image_links'] = product_image_links

                    total_images_count += len(product_image_links)

                    product_name = soup.find("div", class_="col-sm-7").find("h1").text
                    card['product_name'] = product_name

                    table = soup.find("table", class_="table table-bordered table-striped")

                    specifications = {}
                    theads = table.find_all("thead")
                    for thead in theads:
                        title = thead.find("td").text
                        trs = specification_html.find("tbody").find_all("tr")
                        spec = {}
                        for tr in trs:
                            tds = tr.find_all("td")
                            k = tds[0].text
                            v = tds[1].text
                            spec[k] = v
                        specifications[title] = spec

                    card['specifications'] = specifications

                    try:
                        instruction_link = soup.find("span", class_="dname").find("a").get('href')
                    except Exception:
                        instruction_link = None
                    card['instruction_link'] = instruction_link

                    cards.append(card)

                    print(f"Page: {index + 1}/{len(products)} in {subcategory_name_translit} is completed")

                subcategory_dict['subcategory_cards'] = cards
                subcategory_items.append(subcategory_dict)

            category['subcategory_items'] = subcategory_items
            category_items.append(category)

    all_data['category_items'] = category_items
    all_data['total_items_count'] = total_items_count
    all_data['total_images_count'] = total_images_count

    with open("all_data.json", "w", encoding="utf-8") as file:
        json.dump(all_data, file, indent=4, ensure_ascii=False)


def main():
    get_data()


if __name__ == '__main__':
    main()