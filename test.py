#!pip install selenium

#from selenium import webdriver

# Chrome 드라이버 다운로드 및 경로 설정(코랩)
#!apt-get update
#!apt install chromium-chromedriver
#!cp /usr/lib/chromium-browser/chromedriver /usr/bin


# Chrome 드라이버 설정
# options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # 화면 표시 없이 실행
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')


# Chrome 드라이버 초기화
#driver = webdriver.Chrome(options=options)


from bs4 import BeautifulSoup
import  requests
import time


# 웹 페이지 열기
#driver.get("https://select.ridibooks.com/categories/2200?sort=popular&page=1" )
url = "https://select.ridibooks.com/categories/2200?sort=popular&page=1"
#url = "https://ridibooks.com/categories/new-releases/2200"


response= requests.get(url)
response.encoding='utf-8'



#from selenium import webdriver
#from bs4 import BeautifulSoup
#import time



# 페이지의 HTML 가져오기
#html = driver.page_source     # driver.page_source
html= response.text
soup = BeautifulSoup(html, 'html.parser')


# 원하는 데이터 선택
#bookservices = soup.select('h3.GridBookList_ItemTitle')
bookservices = soup.select('.title_text')

# 출력
for no, book in enumerate(bookservices, 1):
    print(no, book.text.strip())

# 브라우저 닫기
#driver.quit()

