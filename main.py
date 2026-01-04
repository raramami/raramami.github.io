from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv
from file import save_to_file


class JobScraper:
    def __init__(self,keyword):
        self.keyword = keyword
        self.job_db = []
        self.content = ""

    def dynamic_scraper(self):
        with sync_playwright() as p:
           
            url = f"https://www.wanted.co.kr/search?query={self.keyword}&tab=position"
            print(f"Hello from python-scrap from {url} !")

            browser = p.chromium.launch(headless=False)  #headless default is True which means the browser will run in the background . 
            page = browser.new_page()
            page.goto(url)
        
            time.sleep(5)

            """
            page.click("button.Aside_searchButton__Ib5Dn")
            time.sleep(5)
            
            #placeholder is the text that is displayed in the input field before the user starts typing.
            #검색시 클래스는 추후 바꿀 수 있으니 플레이스홀더를 사용해서 검색하는 것이 좋다. 

            page.get_by_placeholder("검색어를 입력해 주세요.").fill("flutter")

            time.sleep(5)

            page.keyboard.down("Enter")
            time.sleep(5)

            page.click("a#search_tab_position")"""
            
            # 정적 스크롤 방식 (다운버튼 클릭 수 알고 있어야 )
            # for _ in range(5):
            #     time.sleep(5)
            #     page.keyboard.down("End")

            # 특정요소 갯수를 확인해서 스크롤 처리 => 잘 작동되지 않음 ㅠㅠ
            # prev_cnt = page.locator("JobCard_container__zQcZs").count()
            # while True:
            #     page.keyboard.down("End")
            #     time.sleep(5)
            #     curr_cnt = page.locator("JobCard_container__zQcZs").count()
            #     print(prev_cnt)
            #     print(curr_cnt)
            #     if curr_cnt == prev_cnt:
            #         break
            #     prev_cnt = curr_cnt

            #무한 스크롤 처리 = 브라우저의 실제 높이 확인하면서 처리하는 playwright 의 page.evaluate 사용 => 잘 작동됨 
            prev_height = page.evaluate("document.body.scrollHeight")
            while True:
                page.keyboard.down("End")
                time.sleep(5)
                curr_height = page.evaluate("document.body.scrollHeight")
                if prev_height == curr_height:
                    break
                prev_height = curr_height
                #print(f"Scrolling ... current height : {curr_height}")

            self.content = page.content()
            browser.close()
        

    def parse(self):
        soup = BeautifulSoup(self.content, "html.parser")
        jobs_list = soup.find_all("div", class_="JobCard_container__zQcZs")

        for job in jobs_list:
            link = f"https://wanted.co.kr{job.find('a')['href']}"
            position = job.find("a")["data-position-name"]
            company = job.find("a")["data-company-name"]
            title = job.find("strong", class_="JobCard_title___kfvj").text
            period = job.find("span", class_="CompanyNameWithLocationPeriod_CompanyNameWithLocationPeriod__location__4_w0l").text
            reward_tag = job.find("span", class_="JobCard_reward__oCSIQ")
            reward = reward_tag.get_text(strip=True) if reward_tag else "No reward!"
        
            job = {
                "title": title,
                "company": company,
                "position": position,
                "period": period,
                "reward": reward,
                "link": link,
            }
            self.job_db.append(job)
        
        
    def save_csv(self):
        with open(f"{self.keyword}.csv","w") as file:
            writer = csv.writer(file)
            writer.writerow(["title","company","position","period","reward","link"]) #header
            for j in self.job_db:
                writer.writerow(j.values())
            file.close()

    
   

if __name__ == "__main__":
    keywords = (
        "nextjs",
        "flutter",
        "java",
        )
    for k in keywords:
        scraper = JobScraper(k)
        scraper.dynamic_scraper()
        scraper.parse()
        scraper.save_csv()