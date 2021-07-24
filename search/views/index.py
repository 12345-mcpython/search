import time

from flask import Blueprint, render_template, request, redirect

from search.config.config import Config
from search.database.mysql import Simple

a = Blueprint("index", __name__, template_folder="index")


class Text:
    def __init__(self, url, title):
        self.url = url
        self.title = title


@a.route("/")
def index():
    return render_template("index.html")


@a.route("/search")
def so():
    current_page = request.args.get("page", 1)
    current_page = int(current_page)
    start1 = (current_page - 1) * 20  # 10 20 (current_page-1)*10
    end1 = current_page * 20  # 20 30  current_page*10
    # print(start1, end)
    if not request.args.get("q") or " " in request.args.get("q"):
        return redirect("/")
    start = time.time()
    sql = Simple(Config.MYSQL['MYSQL_HOST'], Config.MYSQL["MYSQL_PORT"], Config.MYSQL['MYSQL_USER'],
                 Config.MYSQL['MYSQL_PASSWORD'], "so")
    data_base = sql.query_data("so_backup", "title,url")
    q = request.args.get("q")
    data_ = []
    for title, url in data_base:
        if q in title:
            data_.append(Text(url, title))
    data = data_[start1:end1]
    end = round(time.time() - start, 2)
    page_next = "http://127.0.0.1:5000/search?q=" + request.args.get("q").split("?")[0] + "&page=" + str(
        current_page + 1)
    page_prep = "http://127.0.0.1:5000/search?q=" + request.args.get("q").split("?")[0] + "&page=" + str(
        current_page - 1)
    return render_template("search.html", result=data, count=len(data_), time_cost=end,
                           title=request.args.get("q").split("?")[0], has_next=end1 < len(data_), page_next=page_next,
                           has_prep=current_page != 1, page_prep=page_prep)
