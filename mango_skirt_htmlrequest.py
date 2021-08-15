import json
from requests_html import HTMLSession

url = "https://shop.mango.com/bg-en/women/skirts-midi/midi-satin-skirt_17042020.html?c=99"

session = HTMLSession()


def request_url(url_item):
    """Get request of the given url and render the page and executes the JavaScript"""
    request = session.get(url_item)
    request.html.render(sleep=1)
    return request


def parse(product_request):
    """Parse the information from the request using css selectors and xpath."""
    request = request_url(url)
    name = request.html.find("h1.product-name", first=True).text
    price = request.html.xpath('//*[@id="app"]/main/div/div[3]/div[1]/div[2]/meta[2]/@content')[0]
    color = request.html.find("span.colors-info-name", first=True).text
    sizes_request = request.html.find("span.size-available")
    sizes = []

    """Loop through all available sizes"""
    for size in sizes_request:
        sizes.append(size.text)

    product_data = {
        "name": name,
        "price": float(price),
        "color": color,
        "sizes": sizes
    }
    return product_data


def output(data):
    """Output the data as json file"""
    with open("skirt_data.json", "w") as outfile:
        json.dump(data, outfile)


product = request_url(url)
output(parse(product))
