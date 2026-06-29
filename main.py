from imports import *


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/homepage")
def homepage():
    return render_template("homepage.html")

@app.route("/account_create", methods=['GET', 'POST'])
def account_create():
    # if request.method == "POST":
    #     if 'account-name' in request.form:
    if request.method == "POST":
        if 'account_name' in request.form:
            input_name = request.form.get('account_name')
            input_password = request.form.get('account_password')

            conaccounts = sqlite3.connect('database/account_password.db') # 将指定的数据库连接到 Python 变量
            accountscursor = conaccounts.cursor() # 将 Python 变量指定为数据库的“游标”
            # accountscursor.execute("SELECT * FROM accountinfo") # 要运行 SQL 代码并从数据库中收集特定信息，请使用 `(游标名称).execute(FROM (数据库) (此处填写 SQL 代码))`
            # allaccinfo = accountscursor.fetchall() # 这将收集 SQL 命令返回的所有信息(搜集信息)
            
            accountscursor.execute(
                "INSERT INTO accountinfo (accountemail, accountpassword) VALUES(?,?)", 
                (input_name, input_password) 
            )
            conaccounts.commit()
            conaccounts.close()
            
    return render_template("account_create.html")


# {asdf--

@app.route("/account-create_password")
def account_create_password():
    return render_template('account_create_password')

@app.route("/resources")
def resources():
    return render_template("resources.html")

@app.route("/post")
def post():
    return render_template("postpage.html")

@app.route("/subjectpick")
def subjectpick():
    return render_template("subjectpick_main.html")




if __name__ == "__main__":
    '''if t'''
    app.run(debug=True, port=1234)
