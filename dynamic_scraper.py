from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

#from Gemini
class JobScraper:
    def __init__(self, keyword):
        self.keyword = keyword
        self.job_db = []
        self.content = "" # 결과를 담을 변수

    def dynamic_scraper(self):
        # 1. playwright를 컨텍스트 매니저로 실행
        with sync_playwright() as p:
            url = f"https://www.wanted.co.kr/search?query={self.keyword}&tab=position"
            print(f"--- Scraping Start: {self.keyword} ---")

            # 2. 브라우저 실행
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url)
            
            # 초기 로딩 대기
            time.sleep(5)

            # 3. 무한 스크롤 로직
            prev_height = page.evaluate("document.body.scrollHeight")
            while True:
                page.keyboard.down("End")
                time.sleep(3) # 스크롤 후 로딩 대기
                curr_height = page.evaluate("document.body.scrollHeight")
                if prev_height == curr_height:
                    break
                prev_height = curr_height

            # 4. 페이지 소스를 인스턴스 변수에 저장 후 브라우저 닫기
            self.content = page.content()
            browser.close() 

    def parse(self):
        if not self.content:
            print(f"No content found for {self.keyword}")
            return

        soup = BeautifulSoup(self.content, "html.parser")
        jobs_list = soup.find_all("div", class_="JobCard_container__zQcZs")

        for job in jobs_list:
            try:
                anchor = job.find('a')
                link = f"https://wanted.co.kr{anchor['href']}"
                position = anchor.get("data-position-name", "N/A")
                company = anchor.get("data-company-name", "N/A")
                title = job.find("strong", class_="JobCard_title___kfvj").get_text(strip=True)
                
                # 위치/기간 정보 태그 확인
                period_tag = job.find("span", class_="CompanyNameWithLocationPeriod_CompanyNameWithLocationPeriod__location__4_w0l")
                period = period_tag.get_text(strip=True) if period_tag else "N/A"
                
                reward_tag = job.find("span", class_="JobCard_reward__oCSIQ")
                reward = reward_tag.get_text(strip=True) if reward_tag else "No reward!"
            
                self.job_db.append({
                    "title": title,
                    "company": company,
                    "position": position,
                    "period": period,
                    "reward": reward,
                    "link": link,
                })
            except Exception as e:
                print(f"Error parsing a job item: {e}")
        
    def save_csv(self):
        if not self.job_db:
            return
            
        # encoding='utf-8-sig'를 쓰면 엑셀에서 한글이 깨지지 않습니다.
        with open(f"{self.keyword}.csv", "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(["title", "company", "position", "period", "reward", "link"])
            for j in self.job_db:
                writer.writerow(j.values())
        print(f"--- Saved {len(self.job_db)} jobs for '{self.keyword}' ---")

if __name__ == "__main__":
    keywords = ("java", "flutter", "kotlin")
    
    for k in keywords:
        scraper = JobScraper(k)
        scraper.dynamic_scraper()
        scraper.parse()
        scraper.save_csv()