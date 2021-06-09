import requests
from bs4 import BeautifulSoup
import csv
from send_email import send

#header for request
headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}

stock_heads = ["Stock Name", "Current Price", "Previous Close", "Open", "Bid", "Ask", "Day's Range", "52 Week Range", "Volume", "avg Volume"]

#read from urls.csv
urls = []
urlname = "urls.csv"
csv_urls = open(urlname, "r")
reader = csv.reader(csv_urls)
for s in reader:
    urls.append(s[1])



filename = "data/stockinfo.csv"
csv_f = open(filename, "w+")
csv_writer = csv.writer(csv_f)
csv_writer.writerow(stock_heads)

for url in urls:
    html_page = requests.get(url, headers=headers)

    soup = BeautifulSoup(html_page.content, "lxml")

    # title_html = soup.find("title")
    # title = title_html.get_text()
    #inspect the html code first find which html tag contains the information
    stock_info = soup.find_all("div", id = "quote-header-info")[0]
    stock_title = stock_info.find("h1").get_text()
    stock_price = stock_info.find("div", class_="D(ib) Mend(20px)").find("span").get_text()

    stock_table = soup.find_all("table")[0].find_all("tr")

    table = []
    for item in stock_table:
        data = item.find_all("td")
        info = data[1].get_text() #data[0] is the catergory name
        table.append(info)

    stock = []
    stock.append(stock_title)
    stock.append(stock_price)

    for item in table:
        stock.append(item)
    
    csv_writer.writerow(stock)

csv_f.close()

send(filename = filename)