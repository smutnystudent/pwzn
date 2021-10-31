import rich.traceback
import requests
from bs4 import BeautifulSoup
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help="nazwa pliku", default="lista odcinków")
args = parser.parse_args()
rich.traceback.install()
req = requests.get('https://www.imdb.com/title/tt0773262/episodes?season=1')
soup = BeautifulSoup(req.text, 'html.parser')
episodes_list = soup.find('div', class_ = 'list detail eplist')
episodes = episodes_list.find_all('div', class_ = 'list_item')
with open(args.file + '.json', 'w') as f:
    for ep in episodes:
        json.dump((ep.find('a').text.strip()), f)
        episodes1 = ep.find_all('div', class_='info')
        for eps1 in episodes1:
            json.dump((eps1.find('a').text.strip()), f)
