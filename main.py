from flask import Flask, render_template, request, redirect, send_file
from Saramin_Scrapper import get_jobs as get_saramin_jobs
from Jobkorea_Scrapper import get_jobs as get_jobkorea_jobs
from exporter import save_to_file


# 앱만들기 시작 !

# fake DB
db = {}

# 앱 이름이 SuperScrapper임
app = Flask("SuperScrapper")

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/report")
def report():
  #print(request.args.get("word"))
  #print(request.args)
  
  # args=> url에 담겨져오는 정보
  word = request.args.get("word")

  #리다이렉트
  if word is None:  
    return redirect("/")

  word = word.lower() 

  # radio 체크된 값
  howto = request.args.get('howto')

  existingJobs = db.get(word)
  if existingJobs: 
    jobs = existingJobs
  else:
    if howto == "Jobkorea":
      jobs = get_jobkorea_jobs(word)
    elif howto == "Saramin":
      jobs = get_saramin_jobs(word)
    elif howto == "Both":
      jobs = get_jobkorea_jobs(word)
      jobs.extend(get_saramin_jobs(word))
    else:
      return redirect("/")
        
  db[word] = jobs

  print(jobs)

  return render_template("report.html", searchingBy = word, count = len(jobs), jobs = jobs )

@app.route("/export")
def export():
  try:
    word = request.args.get("word")
    if not word:
      raise Exception()
    word = word.lower()
    jobs = db.get(word)
    if not jobs:
      print(f"검색된 {word}인 job이 존재하지 않습니다.")
      raise Exception()
    
    save_to_file(jobs)

    return send_file('jobs.csv',mimetype='text/csv', attachment_filename= f'{word}Jobs.csv',as_attachment=True)

  except:
    return redirect("/")


# repl 환경에 있으니까 host = 0.0.0.0 서버를 구축한 샘
app.run(host="0.0.0.0")

