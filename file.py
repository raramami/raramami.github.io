from extractors.berlin import extractors_berlin_jobs
from extractors.wwr import extractors_wwr_jobs 
from extractors.web3 import extractors_web3_jobs
#from main import JobScraper
# from file import save_to_file

#keyword = input("What do you want to search for ?")


# scraper = JobScraper(keyword)
# scraper.dynamic_scraper()
# scraper.parse()
# scraper.save_csv()

def save_to_file(file_name,jobs):
    with open(f"{file_name}.csv","w") as file:
            file.write("Company,Job Title,URL\n")
           
            for job in jobs:
                file.write(f"{job['company_name']},{job['job_titles']},{job['company_url']}\n")          
            file.close()