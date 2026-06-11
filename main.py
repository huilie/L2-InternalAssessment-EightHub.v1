from imports import *


@app.route("/")
def home():
    return render_template("index.html")



@app.route("/homepage")
def homepage():
    return render_template("homepage.html")

@app.route("/account-create")
def account_create():
    return render_template("account-create.html")

@app.route("/resources")
def resources():
    return render_template("resources.html")

@app.route("/post")
def post():
    return render_template("postpage.html")

@app.route("/subjectpick")
def subjectpick():
    return render_template("subjectpick-main.html")




if __name__ == "__main__":
    '''if t'''
    app.run(debug=True)