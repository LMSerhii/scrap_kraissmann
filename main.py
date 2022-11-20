import requests

from bs4 import BeautifulSoup


def get_data():
    """ """
    all_url = []
    category_list = []

    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    url = "https://kraissmann.com/akumulyatorni-instrumenti/"

    response = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(response.text, "lxml")
    subcategories = soup.find_all("div", class_="col-sm-3 catimg")
    all_data = []
    subcategory_link_to_images = []
    for subcategory in subcategories[:1]:
        subcategory_link_to_image = subcategory.select_one("a img").get("src")
        subcategory_link_to_images.append(subcategory_link_to_image)

        subcategory_link = subcategory.select_one('a').get('href')
        subcategory_name = subcategory_link.split("/")[-2]
        # print(subcategory_name)

        with requests.Session() as session:

            response = session.get(url=subcategory_link, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            products = soup.find_all("div", class_="product-thumb")
            cards = []
            for product in products[:1]:

                product_link = product.select_one("div.caption").select_one("h4 a").get('href')
                # print(product_link)

                response = session.get(url=product_link, headers=headers)
                soup = BeautifulSoup(response.text, 'lxml')

                product_name_translit = product_link.split("/")[-1]
                # print(product_name)

                specification_html = soup.find("div", id="tab-specification")
                # print(specification)

                description_html = soup.find("div", id="tab-description")
                # print(description)

                images_links_search = soup.find("ul", class_="thumbnails").find_all("li")
                product_image_links = [link.find("a").get('href') for link in images_links_search]
                # print(product_image_links)

                product_name = soup.find("div", class_="col-sm-7").find("h1").text
                print(product_name)

                specification = {}
                trs = specification_html.find("tbody").find_all("tr")
                for tr in trs:
                    tds = tr.find_all("td")
                    k = tds[0].text
                    v = tds[1].text
                    print(f"{k} - {v}")


def main():
    get_data()


if __name__ == '__main__':
    main()