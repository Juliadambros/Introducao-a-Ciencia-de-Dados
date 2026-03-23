from bs4 import BeautifulSoup
import requests

url = "https://term.ooo/"

html = requests.get(url).text

print(html)
print("------------------------------")

soup = BeautifulSoup(html, 'html5lib')

print(soup)
print("------------------------------")

important_paragraphs = soup('p', {'class': 'important'})

spans_inside_divs = [
    span
    for div in soup('div')
    for span in div('span')
]

print(important_paragraphs)
print("------------------------------")
print(spans_inside_divs)