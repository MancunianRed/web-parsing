from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import json
ua = UserAgent()
header = {"user-agent": ua.random}


link = "https://www.rina.org/en/media/News"
res = requests.get(link, headers=header)
new_link_list = []
soup = BeautifulSoup(res.text, "html.parser")
divs = soup.find_all("div", class_="media-body")

with open("old_news_rina.txt", "r+") as file:
    files = file.read().splitlines()
    for div in divs:
        if (link := div.find("a")["href"]) in files:
            continue
        else:
            new_link_list.append(link)
            file.write(link + "\n")

data = {}

for index,  new_link in enumerate(new_link_list, 1):
    url = f"https://www.rina.org{new_link}"
    r = requests.get(url, headers=header)
    s = BeautifulSoup(r.text, "html.parser")
    head = s.find("div", class_="col-md-9").text.strip()
    div = s.find("div", class_="col-xs-12")
    date = div.find("h2").text.strip()
    sub_head = div.find("h2", class_="press-subtitle").text.strip()
    text = div.find_all("p")
    full_text = ""
    for p in text:
        full_text = full_text + p.text.strip() + " "
    data[index] = {"head": head, "date": date,
                   "sub_head": sub_head, "text": full_text}


with open("data_file_rina.json", "w") as write_file:
    json.dump(data, write_file)