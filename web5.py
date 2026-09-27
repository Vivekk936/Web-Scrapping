import requests
from bs4 import BeautifulSoup
import csv
def Extract(url):
    response = requests.get(url=url).content
    soup = BeautifulSoup(response, 'lxml')
    tag=soup.find("div",{"class":"position-relative cleared z-index-50 background-white"})
    h=tag.find_all("div")
    content=[p.text for p in h]

    with open('data.csv','w') as csv_files:
        csv_write=csv.writer(csv_files)
        csv_write.writerow(content)

Extract(url="https://www.nature.com/")
