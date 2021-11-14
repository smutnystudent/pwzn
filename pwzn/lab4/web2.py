import argparse
import json
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help="nazwa pliku", default="dexter")
args = parser.parse_args()
options = Options()
options.add_argument('--disable-notifications')
service = Service('./chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://www.imdb.com/')
search_bar = driver.find_element_by_name("q")
search_bar.send_keys("dexter")
search_bar.send_keys(Keys.RETURN)
link = driver.find_element_by_link_text('Dexter')
link.click()
button = driver.find_element_by_link_text('Episode guide')
button.click()
req = requests.get(driver.current_url)
soup = BeautifulSoup(req.text, 'html.parser')
episodes_list = soup.find('div', class_='list detail eplist')
episodes = episodes_list.find_all('div', class_='list_item')
eps = []
for ep in episodes:
    eps.append((ep.find('a').text.strip()))
    episodes1 = ep.find_all('div', class_='info')
    for eps1 in episodes1:
        eps.append((eps1.find('a').text.strip()))
with open(args.file + '.json', 'w') as file:
    json.dump(eps, file)