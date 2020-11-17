from flask import Flask, render_template, request, redirect
from scrapper import get_jobs

app = Flask("SuperScrapper")


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
        jobs = get_jobs(word)
        print(jobs)
    else:
        # 입력받은 것이 없을 경우 home으로 redirect
        return redirect("/")

    # rendering (변수를 전달)
    return render_template("report.html", searchingWord=word)


app.run(host="0.0.0.0")
