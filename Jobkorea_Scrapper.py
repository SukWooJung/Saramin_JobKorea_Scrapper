import requests
from bs4 import BeautifulSoup

def get_last_page(url):
  html_text = requests.get(url)
  htmls = BeautifulSoup(html_text.text, "html.parser")
  pagination = htmls.find("div",{"class":"tplPagination"})
  results = pagination.find_all("li")
  pages=[]
  for result in results[1:10]:
    pages.append(int(result.find("a").string))
  
  return pages[-1]

  
def extract_jobs(last_page, url):
  # 1페이지 부터 ~ last_page까지
  jobs=[]
  for page in range(last_page):
    print(f"{page+1}페이지 출력합니다.")
    html_text = requests.get(f"{url}&Page_No={page+1}") 
    htmls = BeautifulSoup(html_text.text, "html.parser")
    items = htmls.find_all("li",{"class":"list-post"}) 
    # items는 한 페이지에 올라온 모든 직업공고 htmls가 담겨짐
    
    for item in items:
      job = extract_job(item) 
      if not job == {}:
       jobs.append(job)

  return jobs

def extract_job(item):
  # title
  post_list_info = item.find("div", {"class":"post-list-info"})
  title =""
  try: 
    title = post_list_info.find("a")["title"] 
  
  except:
    return {}
  #company
  company = item.find("div", {"class":"post-list-corp"}).find("a")["title"]
  
  # location
  option = post_list_info.find("p",{"class":"option"})
  
  try:
    location = option.find("span",{"class":"loc long"}).string
  except:
    return {}
  
  # qualification  
  qualification = ""
  all_span = option.find_all("span")
  for span_html in all_span[0:2]:
    qualification += span_html.string + " "

  
  # position
  position = all_span[2].string
  
  # division
  division = ""
  
  # link 
  data_gno = item["data-gno"]
  link = f"http://www.jobkorea.co.kr/Recruit/GI_Read/{data_gno}"
 
  return {"title":title, "company":company, "location":location, "qualification":qualification, "position":position, "division":division, "link":link}


def get_jobs(word):
  url = "http://www.jobkorea.co.kr/Search/?stext={word}&tabType=recruit"
  last_page = get_last_page(url)
  jobs = extract_jobs(last_page, url)

  return jobs
    
  