from imports import *

app.secret_key = "awdawdawd"
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/account_create", methods=['GET', 'POST'])
def account_create():
    if "back" in request.form:
            return redirect(url_for("index"))
    if request.method == "POST":
        if 'account_name' in request.form:
            input_name = request.form.get('account_name')
            session["input_name"] = input_name  # 把变量 email 的值保存起来，并命名为 "email"，以后这个用户访问其他页面时都可以取出来
        if not input_name:
                return render_template(
                    "account_create.html",
                    create_password_error="pls input email"
                )
        return redirect(url_for('account_create_password'))
        # 将变量提前储存
    return render_template("account_create.html")


@app.route("/account_create-password", methods=['GET', 'POST'])
def account_create_password():
    if "back" in request.form:
         return redirect(url_for("account_create"))
    if request.method == "POST":
        if 'account_password' in request.form:
            input_password = request.form.get('account_password')
            ensure_input_password = request.form.get('ensure_account_password')
            input_name = session.get("input_name")
            if input_password != ensure_input_password:
                return render_template(
                    "account_create_password.html",
                    create_password_error="pls check ur password is same"# error feedback
                    )
            if not input_password or not ensure_input_password:
                return render_template(
                    "account_create_password.html",
                    create_password_error="pls input password"
                )

            conaccounts = sqlite3.connect('database/account_password.db')
            accountscursor = conaccounts.cursor()
            accountscursor.execute(
                "INSERT INTO accountinfo (accountemail, accountpassword) VALUES(?,?)", 
                (input_name, input_password) 
            )
            
            conaccounts.commit()
            conaccounts.close()
        return render_template('homepage.html')
    return render_template('account_create_password.html')


@app.route("/homepage", methods=['GET', 'POST'])
def homepage():
    return render_template("homepage.html")




@app.route("/resources", methods=['GET', 'POST'])
def resources():
    return render_template("resources.html")




@app.route("/post", methods=['GET', 'POST'])
def post():
    return render_template("postpage.html")











@app.route("/subjectpic/<int:subject_id>", methods=['GET','POST'])
def subjectpick(sub_id):
    if request.method == "POST":
        sub_id = request.form.get("subject")
        consubject = sqlite3.connect('database/subject.db')
        sub_cursor = consubject.cursor()
        sub_cursor.execute(
            "SELECT * FROM unit WHERE sub_id=?",
            (sub_id)
            )
        return render_template("subjectpick_unity.html")
    return render_template("subjectpick_main.html")


@app.route("/unit/<int:unit_id>", methods=['GET','POST'])
def unit(unit_id):
    if request.method == "POST":
        su
    return render_template("subjectpick_unity.html")





@app.route("/subjectpick_unity_mathsl1", methods=['GET', 'POST'])
def subjectpick_unity_mathsl1():
    
    return render_template("subjectpick_unity_mathsl1.html")



@app.route("/subjectpick_unity_mathsl2", methods=['GET', 'POST'])
def subjectpick_unity_mathsl2():
    return render_template("subjectpick_unity_mathsl2.html")



@app.route("/subjectpick_unity_mathsl3", methods=['GET', 'POST'])
def subjectpick_unity_mathsl3():
    return render_template("subjectpick_unity_mathsl3.html")





if __name__ == "__main__":
    '''if t'''
    app.run(debug=True, port=1234)
