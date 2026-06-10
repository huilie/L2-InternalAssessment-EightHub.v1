from flask import Flask, render_template

app = Flask (__name__)

@app.route("/")
def index():
    return remder_template("index.html")

@app.route("/homepage")
def homepage():
    return remder_template("homepage.html")


@app.route("/account-create")
def account_create():
    return remder_template("account-create.html")

@app.route("/resources")
def resources():
    return remder_template("resources.html")

@app.route("/post")
def post():
    return remder_template("postpage.html")

@app.route("/subjectpick")
def subjectpick():
    return remder_template("subjectpick-main.html")




if __name__ == "__main__":
    '''if t'''
    app.run(debug=True)