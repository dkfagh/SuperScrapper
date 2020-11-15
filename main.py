from flask import Flask, render_template, request

app = Flask("SuperScrapper")


# @ = decorator
# 바로 아래에 있는 함수를 찾아서 실행
@app.route("/")
def home():
    return render_template("potato.html")


@app.route("/report")
def report():
    # request에서 word라는 이름의 매개변수를 검색
    word = request.args.get('word')
    return render_template("report.html", searchingBy=word)


app.run(host="0.0.0.0")
