import requests
import parsel

content = requests.get('https://merchantpoint.ru/sitemap/brands.xml').content

selector = parsel.Selector(text=content.decode('utf8'))
print(selector)
locs = selector.xpath('//loc/text()').getall()
print(locs)
