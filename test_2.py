# balchun_9_wdm.py ((크롬매니저)이용)

import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
)

# --- 1) Chrome 옵션 (Headless 포함)
chrome_options = Options()
# 최신 크롬 기준 headless 권장 플래그
chrome_options.add_argument("--headless=new")   # 디버깅 시 주석
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
# 필요시 바이너리 경로 지정(일반적으로 불필요)
# chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# --- 2) WebDriver 초기화 (webdriver-manager로 드라이버 자동 설치/관리)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# --- 3) 대상 URL 접속
url = "https://page.kakao.com/content/57540287"
driver.get(url)

# 첫 로딩 안정화
WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
time.sleep(2)

# --- 4) '더보기' 버튼 반복 클릭 (인덱스 기반)
def click_more_repeatedly(start_index=26, step=25, max_clicks=999):
    """
    Kakao Page 댓글 섹션에서 '더보기' 버튼을 인덱스로 찾아가며 반복 클릭.
    페이지 구조가 변하면 XPath를 조정해야 함.
    """
    more_button_xpath_template = (
        '//*[@id="__next"]/div/div[2]/div[1]/div/div[2]/div[2]/div[3]/div/div[2]/div[{}]/img'
    )
    index = start_index
    clicks = 0

    while clicks < max_clicks:
        try:
            xpath = more_button_xpath_template.format(index)
            btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            # 클릭 전 스크롤 가시화
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            time.sleep(0.2)
            try:
                btn.click()
            except ElementClickInterceptedException:
                driver.execute_script("arguments[0].click();", btn)

            time.sleep(1.5)  # 로드 대기
            index += step
            clicks += 1
        except (TimeoutException, StaleElementReferenceException) as e:
            print("더 이상 '더보기' 버튼이 없거나 클릭 불가:", e.__class__.__name__)
            break
        except Exception as e:
            print("예상치 못한 클릭 오류:", repr(e))
            break

click_more_repeatedly()

# --- 5) 댓글 컨테이너 수집
containers_xpath = '//*[@id="__next"]/div/div[2]/div[1]/div/div[2]/div[2]/div[3]/div/div[2]/div'
containers = driver.find_elements(By.XPATH, containers_xpath)
print(f"댓글 컨테이너 수: {len(containers)}")

# --- 6) 댓글 정보 추출
data = []
for idx, container in enumerate(containers, start=1):
    # 댓글내용
    try:
        comment_elem = container.find_element(
            By.CSS_SELECTOR,
            "span.font-medium2.whitespace-pre-wrap.text-el-70.break-word-anywhere"
        )
        comment_text = comment_elem.text.strip()
    except Exception as e:
        comment_text = ""
        print(f"[{idx}] 댓글내용 추출 오류:", e)

    # 닉네임
    try:
        nickname = container.find_element(
            By.XPATH, ".//div/div[1]/div[2]/div[1]/span[1]"
        ).text.strip()
    except Exception as e:
        nickname = ""
        print(f"[{idx}] 닉네임 추출 오류:", e)

    # 회차수
    try:
        round_number = container.find_element(
            By.XPATH, ".//div/div[1]/div[2]/div[2]/div[1]/span[2]"
        ).text.strip()
    except Exception as e:
        round_number = ""
        print(f"[{idx}] 회차수 추출 오류:", e)

    # 좋아요(개수)
    try:
        likes = container.find_element(
            By.XPATH, ".//div/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/span"
        ).text.strip()
    except Exception as e:
        likes = ""
        print(f"[{idx}] 좋아요 추출 오류:", e)

    # 대댓글(개수)
    try:
        reply_count = container.find_element(
            By.XPATH, ".//div/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/span"
        ).text.strip()
    except Exception as e:
        reply_count = ""
        print(f"[{idx}] 대댓글 추출 오류:", e)

    # 작성일
    try:
        date = container.find_element(
            By.XPATH, ".//div/div[1]/div[2]/div[1]/span[2]"
        ).text.strip()
    except Exception as e:
        date = ""
        print(f"[{idx}] 작성일 추출 오류:", e)

    data.append(
        {
            "번호": idx,
            "닉네임": nickname,
            "댓글내용": comment_text,
            "회차수": round_number,
            "좋아요(개수)": likes,
            "대댓글(개수)": reply_count,
            "작성일": date,
        }
    )

df_bc_9 = pd.DataFrame(data)
df_bc_9 = df_bc_9[
    ["번호", "닉네임", "댓글내용", "회차수", "좋아요(개수)", "대댓글(개수)", "작성일"]
]
print(df_bc_9)

# --- 9) 저장
df_bc_9.to_csv("df_bc_9.csv", index=False, encoding="utf-8-sig")
print("DataFrame이 'df_bc_9.csv'로 저장되었습니다.")
df_bc_9.to_csv("df_bc_9.txt", index=False, sep="\t", encoding="utf-8-sig")
print("DataFrame이 'df_bc_9.txt'로 저장되었습니다.")

# --- 8) 종료
driver.quit()
