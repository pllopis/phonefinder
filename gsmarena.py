from bs4 import BeautifulSoup
import requests
import json
import re

page = requests.get('https://www.gsmarena.com/battery-test.php3')
soup = BeautifulSoup(page.content, 'html.parser')

data = []
tbody = soup.find('tbody')
rows = tbody.find_all('tr')
for row in rows:
    columns = row.find_all('td')
    score = columns[1].get_text().strip()
    score = int(re.sub(r'[^0-9]', '', score))
    item = { 'name': columns[0].get_text().strip(), 'score': score}
    name_bare = re.sub(r'\([^()]*\)', '', item['name']) # remove anything in parenthesis
    name_bare = re.sub(r'5G', '', item['name']) # remove anything in parenthesis
    name_bare = name_bare.strip()
    item['name_bare'] = name_bare
    data.append(item)

print(json.dumps(data, indent=4))
