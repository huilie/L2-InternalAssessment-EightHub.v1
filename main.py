from imports import *


@app.route("/")
def index():
    return render_template("index.html")


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
            accountscursor.execute(
                "INSERT INTO accountinfo (accountemail, accountpassword) VALUES(?,?)", 
                (input_name, input_password) 
            )
            conaccounts.commit()
            conaccounts.close()

#加一个使用“-”的命名错误并改为“_”


        return redirect(url_for('account_create_password'))
    return render_template("account_create.html")

@app.route("/account_create-password")
def account_create_password():
    if request.method == "POST":
        if 'account_password' in request.form:
            input_password = request.form.get('account_password')
            conaccounts = sqlite3.connect('database/account_password.db')
            accountscursor = conaccounts.suror()
            accountscursor.execute(
                "INSERT INTO accountinfo (accountemail, accountpassword) VALUES(?,?)", 
                (input_password) 
            )
            
            conaccounts.commit()
            conaccounts.close()


    return render_template('account_create_password.html')


@app.route("/homepage")
def homepage():
    return render_template("homepage.html")

# {asdf--



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
