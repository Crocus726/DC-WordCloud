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

    default_link = 'https://gall.dcinside.com/board/' # 갤러리 기본 URL을 지정함
    gall_id = input("갤러리의 ID를 입력해주세요: ") # 갤러리 ID 입력받음(URL)

    req = requests.get(default_link + 'lists/?id=' + gall_id, headers = headers) # 갤러리 메인 페이지에 GET 요청을 보냄

    # 정식 갤러리, 마이너 갤러리 구분(URL 적을 때 필요함)
    if 'location.replace' in req.text:
        default_link = default_link.replace('board/', 'mgallery/board/') # 갤러리 기본 URL을 마이너 갤러리용으로 변경함
        print("마이너 갤러리로 인식되었습니다.")
    elif req.status_code == 200:
        print("정식(메이저) 갤러리로 인식되었습니다.")
    else:
        print("해당 갤러리를 찾을 수 없습니다.")
        exit()

    page_number = int(input("몇 페이지까지 수집하시겠습니까? (숫자만 입력): ")) # 1페이지부터 몇 페이지까지 수집할 건지 결정

    for page in range(1, page_number + 1):
        # HTTP GET Request
        response = requests.get(default_link + "lists?id=" + gall_id +"&page={}".format(page), headers=headers)

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
