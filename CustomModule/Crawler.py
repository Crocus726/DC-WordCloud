import os
import requests
from bs4 import BeautifulSoup as bs4

def Crawl():
    f = open(os.path.join(os.path.dirname(__file__), "../Resource", "data.txt"), mode="w", encoding="utf-8")
    f.write("")
    f.close()
    f = open(os.path.join(os.path.dirname(__file__), "../Resource", "data.txt"), mode="at", encoding="utf-8")

    # User-Agent 설정
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"}

    gall_id = input("갤러리의 ID를 입력해주세요: ") # 갤러리 ID 입력받음(URL)
    page_number = int(input("몇 페이지까지 수집하시겠습니까? (숫자만 입력): ")) # 1페이지부터 몇 페이지까지 수집할 건지 결정

    for page in range(1, page_number + 1):
        # HTTP GET Request
        response = requests.get("https://gall.dcinside.com/board/lists?id=" + gall_id +"&page={}".format(page), headers=headers)

        # response를 HTML화
        html = response.text
        soup = bs4(html, "html.parser")

        titles = soup.findAll("td", {"class":"gall_tit ub-word"})

        for title in titles:
            # 공지, 설문 게시글 예외처리
            if title.find("em", {"class":"icon_img icon_notice"}) or title.find("em", {"class":"icon_img icon_survey"}):
                pass
            else:
                title = title.find('a').text
                f.write(title + '\n')

if __name__ == "__main__":
    Crawl()
