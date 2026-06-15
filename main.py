from imports import *

# con = rjfweurheuw9rje
# cur = con.cursor()

# cur.execute("SQL CODE")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/homepage")
def homepage():
    return render_template("homepage.html")

@app.route("/account-create")
# @app.route("/account-create", ['GET', 'POST'])
def account_create():
    # if request.method == "POST":
    #     if 'password-name' in request.form:
            
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
    app.run(debug=True, port=1234)
