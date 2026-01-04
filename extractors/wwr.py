import requests
from bs4 import BeautifulSoup



url = "https://weworkremotely.com/remote-full-time-jobs"

def get_pages(url):
  response = requests.get(url)
  soup = BeautifulSoup(response.content,"html.parser")

  return len(soup.find("div",class_="pagination").find_all("span",class_="page"))



def extractors_wwr_jobs(keyword):
    all_jobs = []
    print(f"Scraping for {keyword}")
    url = f"https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term={keyword}"
    response = requests.get(
    url,
    headers={
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })
    print(response.status_code)
    soup = BeautifulSoup(response.content, "html.parser")
    jobs_tag = soup.find("div",class_="search-listings__container")
    jobs = (jobs_tag.find_all("li",class_="new-listing-container feature") if jobs_tag else [])
    
    if jobs:
      jobs = jobs[:-1]
   
    for job in jobs:
      title_tag = job.find("div",class_="new-listing__header__title") 
      job_titles = title_tag.text.strip() if title_tag else "No Title"
      company_name = job.find("p",class_="new-listing__company-name").text
      company_url = job.find("div",class_="tooltip--flag-logo").next_sibling("href")

      job_data = {
          "company_name" : company_name,
          "job_titles" : job_titles,
          "company_url" : company_url,
        }
      all_jobs.append(job_data)
     
    return all_jobs


# results = extractors_wwr_jobs("javascript")
# print(results)

