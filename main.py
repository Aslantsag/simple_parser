import re
import json
import requests
import fake_useragent
from bs4 import BeautifulSoup

user = fake_useragent.UserAgent().random
headers = {'user-agent': user}

def get_currence():
    link = 'https://infobs.online/'
    resp = requests.get(link, headers=headers)
    soup = BeautifulSoup(resp.content, 'html.parser')
    content = soup.find(id='header_topline')
    usd = content.findAll("span")[0].text
    eur = content.findAll("span")[1].text
    return usd, eur

def get_pray_time():
    link = 'https://infobs.online/'
    resp = requests.get(link, headers=headers)
    soup = BeautifulSoup(resp.content, 'html.parser')
    content = soup.find(id='navbarSupportedContent')
    times = content.findAll("table", {"class": "div_namaz_times"})[0]
    res = str(times).replace("<br/>", " - ").replace("</td>", "\n")
    return re.sub(r'<.*?>', '', res)

def get_article():
    link = 'https://infobs.online/news.php'
    resp = requests.get(link, headers=headers)
    soup = BeautifulSoup(resp.content, 'html.parser')
    content = soup.find("section", class_='block_body')
    card = content.findAll("div", class_="card")[0]
    btn = card.findAll("a", class_="btn-primary")[0]
    art_id = str(btn.get("href"))[11:]
    art_link = 'https://infobs.online/new.php?id='+art_id
    with open('ids.txt', 'r+') as ids:
        ids_list = ids.read().split()
        if not art_id in ids_list:
            resp = requests.get(art_link, headers=headers)
            soup = BeautifulSoup(resp.content, 'html.parser')
            art_text_div = soup.find("div", class_="container text-center")
            art_title = soup.find("h1").text
            art_text_list = art_text_div.findAll("p")
            art_text = ''
            for p in art_text_list:
                art_text += " "+p.text
            msg = f"\n*{art_title}*\n\n{art_text}"
            send_status = json.loads(send_msg(msg))
            print(send_status["sent"])
            if send_status.get("sent"):
                ids.write(' ' + art_id)


def send_msg(msg):
    url = 'https://eu132.chat-api.com/YOURINSTANCE/sendMessage?token=YOURTOKEN'
    data = {
      "phone": "7XXXXXXXXXX",
      "body": msg
    }
    res = requests.post(url, json=data)
    return res.text

def main():
    currence = f"${get_currence()[0]}, €{get_currence()[1]}"
    pray_time = get_pray_time()
    send_msg(currence)
    send_msg(pray_time)
    get_article()

if __name__ == '__main__':
    main()
