from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
from exporter import save_to_file

app = Flask("SuperScrapper")

# Fake DateBase
db = {}


# @ = decorator
# 바로 아래에 있는 함수를 찾아서 실행
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/report")
def report():
    # request에서 word라는 이름의 매개변수를 검색
    word = request.args.get('word')

    if word:
        # word를 소문자로 변경 (만약 대문자로 입력할 경우를 가정)
        word = word.lower()

        # 입력받은 검색어가 db에 있는지 확인
        existingJobs = db.get(word)

        # 검색한 단어가 db에 저장되어 있다면
        #   = 이전에 검색한 기록이 있다면
        if existingJobs:
            jobs = existingJobs
        else:
            jobs = get_jobs(word)

            # 입력받은 단어에 관한 공고 정보를 db에 저장
            db[word] = jobs

    else:
        # 입력받은 것이 없을 경우 home으로 redirect
        return redirect("/")

    # rendering (변수를 전달)
    return render_template(
        "report.html", resultsNumber=len(jobs), searchingWord=word, jobs=jobs)


@app.route("/export")
def export():
    try:
        word = request.args.get("word")
        
        # Exception(=Error) 강제 발생 -> except 실행
        if not word:
            raise Exception()

        word = word.lower()
        jobs = db.get(word)

        # 내보낼 CSV가 없을 경우 home으로 redirect
        if not jobs:
            raise Exception()

        # CSV writer로 jobs 파일 생성
        save_to_file(jobs)

        # as_attachment : 파일명 그대로 다운
        # chrome은 안되고 edge에서는 됨
        return send_file("jobs.csv", as_attachment=True)

    except:
        return redirect("/")


app.run(host="0.0.0.0")
