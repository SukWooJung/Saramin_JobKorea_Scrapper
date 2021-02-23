import requests
from bs4 import BeautifulSoup

def get_last_page(url):
  html_text = requests.get(url)
  htmls = BeautifulSoup(html_text.text, "html.parser")
  
  pagination = htmls.find("div",{"class":"pagination"})
  
  pages = pagination.find_all("a")
  results = []
 
  for page in pages[0:-1]:
    results.append(page.find("span").string)
 
  return int(results[-1])

def extract_jobs(last_page, url, count):
  # 1페이지 부터 ~ last_page까지
  jobs=[]
  for page in range(last_page):
    print(f"{page+1}페이지 출력합니다.")
    html_text = requests.get(f"{url}&recruitPage={page+1}")
    htmls = BeautifulSoup(html_text.text, "html.parser")
    items = htmls.find_all("div",{"class":"item_recruit"}) 
    # items는 한 페이지에 올라온 모든 직업공고 htmls가 담겨짐
    
    for item in items:
      job = extract_job(item) 
      jobs.append(job)

  return jobs

def extract_job(item):
  # title
  title = item.find("h2", {"class":"job_tit"}).find("a")["title"]
  
  #company
  company = item.find("div",{"class":"area_corp"}).find("a")["title"]

  # location
  job_condition = item.find("div",{"class":"job_condition"})
  job_condition_first_span = job_condition.find("span")
  locations = job_condition_first_span.find_all("a") 
  location = ""
  for location_html in locations:
    location += location_html.string + " " 
  
  # qualification
  job_condition_all_span = job_condition.find_all("span")
  qualification = ""
  for span in job_condition_all_span[1:3]:
    qualification += span.string + " "

  # position
  position = job_condition_all_span[-1].string

  # division
  job_sector = item.find("div",{"class":"job_sector"})
  divisions = job_sector.find_all("a")
  division = ""
  for a in divisions:
    division += a.string + " "

  # link 
  idx = item["value"]
  link = f"https://www.saramin.co.kr/zf_user/jobs/relay/view?isMypage=no&rec_idx={idx}"

  return {"title":title, "company":company, "location":location, "qualification":qualification, "position":position, "division":division, "link":link}


def get_jobs(word):
  count = 30
  url = f"https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword={word}&recruitSort=relation&recruitPageCount={count}"
  last_page = get_last_page(url)
  jobs = extract_jobs(last_page, url, count)

  return jobs
    
  