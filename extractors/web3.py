import requests
from bs4 import BeautifulSoup
import time



def get_pages(keyword):
    base_url = "https://web3.career"
    page = 1

    #while True:
    max_page = 10
    while page <= max_page:
        url = f"{base_url}/{keyword}-jobs?page={page}"
        print(f"Checking page in {page}")
        response = requests.get(url)
        soup = BeautifulSoup(response.content,"html.parser")
        next_button = soup.select_one("li.page-item.next")
  
        if not next_button or "disabled" in next_button.get("class",[]):
            print(f"Last page : {page}")
            return page
        elif page == max_page:
            return page

        page += 1
        time.sleep(0.5)
   
        



def extractors_web3_jobs(keyword):
    all_jobs = []
    total_page = get_pages(keyword)
   
    base_url = "https://web3.career"

    for i in range(total_page):
        url = f"{base_url}/{keyword}-jobs?page={i}"
        response = requests.get(
        url,
        headers={
            "User-Agent":
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
    
        soup = BeautifulSoup(response.content, "html.parser")
        #jobs = soup.find("tbody",class_="tbody").find_all("tr",class_="table_row")
        jobs = soup.select("tr")
        
        for job in jobs:
            name_tag = job.select_one("h3")
            company_name = name_tag.text.strip() if name_tag else "No company name"
            
            title_tag = job.select_one("h2")
            job_titles = title_tag.text.strip() if title_tag else "No Title"
            
            url_tag = job.select_one("a")
            company_url = url_tag.get("href") if url_tag else "No URL"
            
            job_data = {
                "company_name" : company_name,
                "job_titles" : job_titles,
                "company_url" : f"{base_url}{company_url}",
                
                }
            all_jobs.append(job_data)
     
    return all_jobs

# results = extractors_web3_jobs("java")
# print(len(results))