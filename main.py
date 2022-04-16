import requests
import bs4
import csv

'''
* 졸업작품 Campssg 프로젝트에서 사용하기 위한 테스트/시연 용 데이터 크롤링
* 캠핑장 주변 마트에서 판매하는 상품 카테고리 9개를 선정하여 카테고리별로 30개씩 크롤링
* G마켓 베스트에서 상품을 크롤링해왔으나, G마켓 베스트의 이미지로딩이 lazy Loading 으로 되어 있어서 상품 상세정보 페이지로 이동하여 이미지 url 크롤링
* 크롤링해 온 데이터를 csv 파일로 저장하여 MySQL DB에 import
'''

# 카테고리 별 물품 크롤링 url 설정(g마켓 베스트)
url = [["축산", "1", "http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G07&subGroupCode=S089"],
       ["김치/반찬", "2", "http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G07&subGroupCode=S104"],
       ["생수/음료", "3", "http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G07&subGroupCode=S105"],
       ["간편식품", "4", "http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G07&subGroupCode=S106"],
       ["과일/견과", "5", "http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G07&subGroupCode=S103"],
       ["채소", "6", "http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G07&subGroupCode=S147"],
       ["가공식품", "7", "http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G07&subGroupCode=S107"],
       ["생활용품", "8", "http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G08"],
       ["캠핑용품", "9", "http://corners.gmarket.co.kr/BestSellers?viewType=C&largeCategoryCode=100000017"]]

# 크롤링해 온 물품 정보를 저장할 csv 파일 생성 및 쓰기 객체 생성
f = open("./checkList.csv", 'w', newline='')
wtr = csv.writer(f)
wtr.writerow(['category_id', 'product_name', 'product_price', 'product_img_url'])

for URL in url:
    # url 하나씩 읽어와서 크롤링
    html = bs4.BeautifulSoup(requests.get(URL[2]).content, 'html.parser')

    bestlist = html.select('div.best-list')
    box = bestlist[1]
    items = box.select('ul > li') # 베스트 상품 정보 리스트 크롤링

    imgUrl = [] # 상품 상세페이지 주소를 저장할 리스트
    name = [] # 상품명 저장 리스트
    itemPrice = [] # 상품가격 저장 리스트
    img = [] # 이미지 url 저장 리스트

    # 카테고리 별 베스트 상품 30개씩 크롤링
    for idx, item in enumerate(items[:30]):
        title = item.select_one('a.itemname')
        price = item.select_one('div.s-price > strong')
        imgUrl.insert(idx, title["href"])
        name.append(title.get_text())
        itemPrice.append(int(price.get_text()[:-1].replace(',',''))) # 상품 가격 사이의 ','과 끝의 '원'을 제거하고 int 타입으로 변환하여 저장

    # 상품 상세페이지로 이동하여 이미지 url 크롤링
    for Url in imgUrl:
        html = bs4.BeautifulSoup(requests.get(Url).content, 'html.parser')
        box = html.select_one('div.box__viewer-container')
        image = box.select_one('img')
        img.append(image["src"])

    # 크롤링해 온 상품 정보 csv 파일에 저장
    for i in range(30):
        wtr.writerow([URL[1], name[i], itemPrice[i], img[i]])

f.close()