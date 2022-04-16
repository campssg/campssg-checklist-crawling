import requests
import bs4
import csv

url = [["축산", "1", "http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G07&subGroupCode=S089"],
       ["김치/반찬", "2", "http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G07&subGroupCode=S104"],
       ["생수/음료", "3", "http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G07&subGroupCode=S105"],
       ["간편식품", "4", "http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G07&subGroupCode=S106"],
       ["과일/견과", "5", "http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G07&subGroupCode=S103"],
       ["채소", "6", "http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G07&subGroupCode=S147"],
       ["가공식품", "7", "http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G07&subGroupCode=S107"],
       ["생활용품", "8", "http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G08"],
       ["캠핑용품", "9", "http://corners.gmarket.co.kr/BestSellers?viewType=C&largeCategoryCode=100000017"]]

for URL in url:
    html = bs4.BeautifulSoup(requests.get(URL[2]).content, 'html.parser')

    bestlist = html.select('div.best-list')
    box = bestlist[1]
    items = box.select('ul > li')
    imgUrl = []
    order = []
    name = []
    itemPrice = []
    img = []
    for idx, item in enumerate(items[:30]):
        title = item.select_one('a.itemname')
        price = item.select_one('div.s-price > strong')
        imgUrl.insert(idx, title["href"])
        order.append(idx + 1)
        name.append(title.get_text())
        itemPrice.append(int(price.get_text()[:-1].replace(',','')))

    for Url in imgUrl:
        html = bs4.BeautifulSoup(requests.get(Url).content, 'html.parser')
        box = html.select_one('div.box__viewer-container')
        image = box.select_one('img')
        img.append(image["src"])

    print(f"------------{URL[0]}-------------")

    for i in range(30):
        print(f"{order[i]}: {name[i]} {itemPrice[i]} \n {img[i]}")