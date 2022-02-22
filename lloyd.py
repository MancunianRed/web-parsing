from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import json
ua = UserAgent()
header = {"user-agent": ua.random}

link = "https://www.lr.org/en/latest-news/"
res = requests.get(link, headers=header)
new_link_list = []
soup = BeautifulSoup(res.text, "html.parser")
new_links = soup.find_all("a", class_="heading-link search-result-link")

with open("old_news_lloyd.txt", "r+") as file:
    files = file.read().splitlines()
    for link in new_links:
        if link["href"] in files:
            continue
        else:
            new_link_list.append(link["href"])
            file.write(link["href"] + "\n")

data = {}
for index,  new_link in enumerate(new_link_list, 1):
    url = f"https://www.lr.org{new_link}"
    r = requests.get(url, headers=header)
    s = BeautifulSoup(r.text, "html.parser")
    head = s.find("h1", class_="article-heading h2 underline").text.strip()
    date = s.find("p", class_="article-date").text.strip()
    sub_head = s.find("p", class_="sub-heading").text.strip()
    text = s.find("div", class_="block base12").text.strip()
    data[str(index)] = {"head": head, "date": date,
                   "sub_head": sub_head, "text": text}

with open("data_file_lloyd.json", "w") as write_file:
    json.dump(data, write_file)