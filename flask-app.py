import re
#from tkinter import NO
from flask import Flask, redirect, render_template, request ,redirect,send_file
from extractors.berlin import extractors_berlin_jobs
from extractors.wwr import extractors_wwr_jobs
from extractors.web3 import extractors_web3_jobs
from file import save_to_file

app = Flask("JobScraper")
db = {}  #Cache , kind of fake DB . 

@app.route("/")
def home():
    return render_template("home.html", name="Sunny")

@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    #Cache : 속도향상 
    if keyword in db:
        jobs = db[keyword]
    else:
        indeed = extractors_berlin_jobs(keyword)
        wwr = extractors_wwr_jobs(keyword)
        web3 = extractors_web3_jobs(keyword)
        jobs = indeed + wwr + web3
        db[keyword] = jobs
    return render_template("search.html",keyword=keyword,jobs=jobs)

@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword not in db:
        return redirect(f"/search?keyword={keyword}")
    save_to_file(keyword,db[keyword])
    return send_file(f"{keyword}.csv", as_attachment=True)

app.run("0.0.0.0",port=8000,debug=True)
