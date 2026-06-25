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

@app.route("/account-create", methods=['GET', 'POST'])
# @app.route("/account-create", ['GET', 'POST'])
def account_create():
    # if request.method == "POST":
    #     if 'account-name' in request.form:
    if request.method == "POST":
        if 'account-name' in request.form:
            conaccounts = sqlite3.connect('database/account-password.db') # 将指定的数据库连接到 Python 变量
            accountscursor = conaccounts.cursor() # 将 Python 变量指定为数据库的“游标”
            accountscursor.execute("SELECT * FROM accountinfo") # 要运行 SQL 代码并从数据库中收集特定信息，请使用 `(游标名称).execute(FROM (数据库) (此处填写 SQL 代码))`
            allaccinfo = accountscursor.fetchall() # 这将收集 SQL 命令返回的所有信息(搜集信息)
            print(givenname)
            
    return render_template("account-create.html")



@app.route("/account-create-password")
def account_create_password():
    return render_template('account-create-password')

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
