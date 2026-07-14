from imports import *

app.secret_key = "awdawdawd"
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/account_create", methods=['GET', 'POST'])
def account_create():
    if request.method == "POST":
        if 'account_name' in request.form:
            input_name = request.form.get('account_name')
            session["input_name"] = input_name  # 把变量 email 的值保存起来，并命名为 "email"，以后这个用户访问其他页面时都可以取出来
            return redirect(url_for('account_create_password'))
        # 将变量提前储存
    return render_template("account_create.html")


@app.route("/account_create-password", methods=['GET', 'POST'])
def account_create_password():
    if request.method == "POST":
        if 'account_password' in request.form:
            input_password = request.form.get('account_password')
            input_name = session.get("input_name")
            ensure_input_password = request.form.get('ensure_account_password')
            if ensure_input_password != input_name:
                return

            conaccounts = sqlite3.connect('database/account_password.db')
            accountscursor = conaccounts.cursor()
            accountscursor.execute(
                "INSERT INTO accountinfo (accountemail, accountpassword) VALUES(?,?)", 
                (input_name, input_password) 
            )
            
            conaccounts.commit()
            conaccounts.close()
    return render_template('account_create_password.html')


@app.route("/homepage")
def homepage():
    return render_template("homepage.html")

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
