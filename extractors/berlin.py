import requests
from bs4 import BeautifulSoup


# 👇🏻 YOUR CODE 👇🏻:


"""berlinstartupjobs.com 웹사이트용 스크래퍼를 만듭니다.
스크래퍼는 다음 URL을 스크랩할 수 있어야 합니다:
https://berlinstartupjobs.com/engineering/
https://berlinstartupjobs.com/skill-areas/python/
https://berlinstartupjobs.com/skill-areas/typescript/
https://berlinstartupjobs.com/skill-areas/javascript/
첫 번째 URL에는 페이지가 있으므로 pagination 을 처리해야 합니다.
나머지 URL은 특정 스킬에 대한 것입니다. URL의 구조에 스킬 이름이 있으므로 모든 스킬을 스크래핑할 수 있는 스크래퍼를 만드세요.
회사 이름, 직무 제목, 설명 및 직무 링크를 추출하세요.
"""
# BLUEPRINT | DONT EDIT


# /BLUEPRINT

def get_pages(url):
  response = requests.get(
    url,
    headers={
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })
  soup = BeautifulSoup(response.content,"html.parser")
  pages = soup.find("ul",class_="bsj-nav").find_all(class_="page-numbers")
  return len(pages)-1

def show_pages():
  total_pages = get_pages("https://berlinstartupjobs.com/engineering/")
  for x in range(total_pages):
    url = f"https://berlinstartupjobs.com/engineering/page/{x+1}"
    print(f"pagination: {url}")
  

def extractors_berlin_jobs(keyword):
    all_jobs = []
  #skills = ["python", "typescript", "javascript", "rust"]
 
  #for skill in skills:
    url = f"https://berlinstartupjobs.com/skill-areas/{keyword}"
    response = requests.get(
    url,
    headers={
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })
    soup = BeautifulSoup(response.content,"html.parser")

    lists_tag = soup.find("ul",class_="jobs-list-items")
    lists = lists_tag.find_all("li",class_="bjs-jlid") if lists_tag else []

    
    for list in lists:
        company_infos = list.find("a", class_="bjs-jlid__b") 
        job_title = list.find("h4",class_="bjs-jlid__h")
        job_desc = list.find("div",class_="bjs-jlid__description") 
        jobs_data = {
            "company_name" : company_infos.get_text(strip=True),
            "company_url" : company_infos["href"],
            "job_titles" : job_title.get_text(strip=True),
        }

        all_jobs.append(jobs_data)
        
    return all_jobs

  # 호출 및 확인
# show_pages()
#results = extractors_indeed_jobs("python")
#print(f"Total jobs found: {len(results)}")
# for x in range(len(results)):
#   print(results[x])
