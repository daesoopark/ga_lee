from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Chrome 드라이버 설정
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 화면 표시 없이 실행
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Chrome 드라이버 초기화
driver = webdriver.Chrome(options=options)

# 웹 페이지 열기
driver.get("https://select.ridibooks.com/categories/2200?sort=popular&page=1")

# 페이지가 로드되기 위해 잠시 대기 (필요에 따라 시간 조절)
time.sleep(3)

# 페이지의 HTML 가져오기
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# 원하는 데이터 선택
bookservices = soup.select('h3.GridBookList_ItemTitle')

# bookservices 리스트가 비어 있는지 확인
if not bookservices:
    print("bookservices 리스트가 비어 있습니다.")
else:
    # 각 요소에서 텍스트 추출하여 출력
    for no, book in enumerate(bookservices, 1):
        print(no, book.text.strip())  # 각 책 제목을 출력

# 드라이버 종료
driver.quit()
