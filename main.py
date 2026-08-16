from imports import *
# from imports.py import Flask, request, render_template, redirect, url_for, session, sqlite3, re



# Flask Session needs secret_key
app.secret_key = "awdawdawd"

# index page
@app.route("/", methods=['GET', 'POST'])
def index():
        # check submit = next or not 
        if request.form.get("submit") =="next":
             # if ture, go to account_create
             return render_template("account_create.html")
        # display index page
        return render_template("index.html")

# index page
@app.route("/account_create", methods=['GET', 'POST'])
def account_create():
    if "back" in request.form:
            return redirect(url_for("index"))
    if request.method == "POST":
        if 'account_name' in request.form:
            input_name = request.form.get('account_name')
            session["input_name"] = input_name  
            # save the vulme email，and name email to "email", I can take this vulme in next page
        if not input_name:
                return render_template(
                    "account_create.html",
                    create_password_error="Your email address can't be empty"
                )
        if ("@" not in input_name or input_name.startswith("@") or input_name.endswith("@") or "@." in input_name or (".com" not in input_name and ".nz" not in input_name)):
            return render_template(
                "account_create.html",
                create_password_error="You must input a correct email address"
            )
        return redirect(url_for('account_create_password'))
        # 将变量提前储存
    return render_template("account_create.html")


@app.route("/account_create-password", methods=['GET', 'POST'])
def account_create_password():
    if "back" in request.form:
         return redirect(url_for("account_create"))
    if request.method == "POST":
        # 用户不能输入空白，和空格
        if 'account_password' in request.form:
            input_password = request.form.get('account_password')
            ensure_input_password = request.form.get('ensure_account_password')
            input_name = session.get("input_name")
            if input_password != ensure_input_password:
                return render_template(
                    "account_create_password.html",
                    create_password_error="Please check your ensure password is same with your password"# error feedback
                    )
            if not input_password or not ensure_input_password:
                return render_template(
                    "account_create_password.html",
                    create_password_error="Your password can not be empty"
                )
            if len(input_password) < 8:
                return render_template(
                    "account_create_password.html",
                    create_password_error="Your password must be at least 8 characters"
                )
            if not re.search(r"[A-Za-z]", input_password):
                return render_template(
                    "account_create_password.html",
                    create_password_error="Your password must contain letters"
                )
            if not re.search(r"[0-9]", input_password):
                return render_template(
                    "account_create_password.html",
                    create_password_error="Your password must contain numbers"
                )
            conaccounts = sqlite3.connect('database/database.db')
            accountcursor = conaccounts.cursor()
            accountcursor.execute("SELECT * FROM accountinfo WHERE accountemail=?",
                                  (input_name,)
                                  )
            user = accountcursor.fetchone()
            if user:
                conaccounts.close()
                return render_template("account_create_password.html" 
                                       ,create_password_error="This email already exists, please go back"
                                       )
            accountcursor.execute(
                "INSERT INTO accountinfo (accountemail, accountpassword) VALUES(?,?)", 
                (input_name, input_password) 
            )
            conaccounts.commit()
            conaccounts.close()
        return render_template('homepage.html')
    return render_template('account_create_password.html')

# 用户不能输入空白，和空格

@app.route("/account", methods=['GET', 'POST'])
def account():
     if request.method == "POST":
        action = request.form.get("action")
        conaccounts = sqlite3.connect("database/database.db")
        accountcursor = conaccounts.cursor()
        #login
        if action =="login":
             email = request.form.get("login_email")
             password = request.form.get("login_password")
             accountcursor.execute(
                  "SELECT * FROM accountinfo WHERE accountemail=? AND accountpassword=?",
                  (email, password)
             )
             user = accountcursor.fetchone()
             if user:
                session["email"] = email
                conaccounts.close()
                return render_template("account.html", report_message="Login successful")
             conaccounts.close()
             return render_template("account.html", report_message="Your email or password is incorrect")

        # Change Password
            
        elif action == "change_password":
            email = session.get("email")
            if not email:
                conaccounts.close()
                return render_template("account.html", report_message="Please login your account first")
            old_password = request.form.get("old_password")
            new_password = request.form.get("new_password")
            accountcursor.execute(" SELECT * FROM accountinfo WHERE accountemail=? AND accountpassword=?", 
                (email, old_password)
            )
            user = accountcursor.fetchone()
            if not user:
                conaccounts.close()
                return render_template("account.html", report_message="Your original password is incorrect")
            if len(new_password) < 8:
                return render_template("account.html",
                                       report_message="Your password must be at least 8 characters"
                                       )
            if not re.search(r"[A-Za-z]", new_password):
                return render_template("account.html",
                                       report_message="Your password must contain letters"
                                       )
            if not re.search(r"[0-9]", new_password):
                return render_template("account.html",
                                       report_message="Your password must contain numbers"
                                       )

            accountcursor.execute("UPDATE accountinfo SET accountpassword=? WHERE accountemail=?", 
                                  (new_password, email)
                )
            conaccounts.commit()
            conaccounts.close()
            return render_template("account.html", report_message="Password changed successfully")
        # Delete Account

        elif action == "delete_account":
            email = request.form.get("ensure_email")
            password = request.form.get("delete_password")
            accountcursor.execute( "SELECT * FROM accountinfo WHERE accountemail=? AND accountpassword=?", 
                                  (email, password)
                                  )
            user = accountcursor.fetchone()
            if not user:
                conaccounts.close()
                return render_template("account.html", report_message="Your email or password is incorrect")
            accountcursor.execute("DELETE FROM accountinfo WHERE accountemail=?",
                                  (email,)
                                  )
            conaccounts.commit()
            session.clear()
            conaccounts.close()
            return render_template("account.html", report_message="Account deleted.")
        return render_template('account.html')
     return render_template('account.html')




@app.route("/homepage", methods=['GET', 'POST'])
def homepage():
    if request.method =="POST":
        if 'Searchbar_q' in request.form:
            search_input = request.form.get('Searchbar_q')
            if not search_input or not search_input.strip():
                return render_template(
                    "search_results.html",
                    error_resource_text="Your search bar can't be empty or space"
                )
            # 加一个用户不能输入空白，增加搜索范围
            consearch = sqlite3.connect('database/database.db')
            searchcursor = consearch.cursor()
            query_search = f"%{search_input}%" # 什么意思
            searchcursor.execute(
                "SELECT resources_id, unit, subject, resources_name FROM resources WHERE unit LIKE ? OR subject LIKE ? OR resources_name LIKE ?",
                (query_search, query_search, query_search)
            )
            search_results = searchcursor.fetchall()
            return render_template("search_results.html", results = search_results, keywords = search_input)
    return render_template("homepage.html")



@app.route("/search_results", methods=['GET', 'POST'])
def search_results():
    return render_template("search_results.html")




@app.route("/subjectpic/", methods=['GET','POST']) # 让flask判断用户选择的id，然后再让html显示
def subjectpick():
    if request.method == "POST":
        if 'subject' in request.form:
            sub_id = request.form.get('subject')
            return redirect(url_for("unit", sub_id = sub_id))
        return render_template("subjectpick_unity.html")
    return render_template("subjectpick_main.html")




@app.route("/unit/<int:sub_id>", methods=['GET','POST'])
def unit(sub_id):
    consub_id = sqlite3.connect('database/database.db')
    unit_cursor = consub_id.cursor()
    unit_cursor.execute(
         "SELECT unit_id, unit FROM unit WHERE sub_id=?",
        (sub_id,)
    )# SELECT unit_id, unit 不加括号
    units = unit_cursor.fetchall() # 将从database中搜索到的数据取出，并变成python列表
    return render_template("subjectpick_unity.html", units = units, sub_id = sub_id)


@app.route("/resources_list/<int:unit_id>", methods=['GET', 'POST'])
def resources_list(unit_id):
    conre_list = sqlite3.connect('database/database.db')
    re_cursor = conre_list.cursor()
    re_cursor.execute(
         "SELECT resources_id, resources_name, author FROM resources WHERE unit_id = ?",
         (unit_id,)
)
    resources = re_cursor.fetchall()
    conre_list.close()
    return render_template("resources_list.html", resources = resources, unit_id = unit_id)


@app.route("/all_resources", methods=['GET', 'POST'])
def all_resources():
    selected_type = request.args.get("type", "")
    selected_year = request.args.get("released_year", "")
    conre = sqlite3.connect("database/database.db")
    re_cursor = conre.cursor()
    # get type
    re_cursor.execute(
        "SELECT DISTINCT type FROM resources WHERE type IS NOT NULL ORDER BY type"
    )
    types = re_cursor.fetchall()
    #get realsed year
    re_cursor.execute(
        "SELECT DISTINCT released_year FROM resources WHERE released_year IS NOT NULL ORDER BY released_year"
    )
    years = re_cursor.fetchall()
    #筛选查询
    search_sql = "SELECT resources_id, subject, unit, resources_name, path, type, author, released_year FROM resources WHERE 1=1"
    parameters = []
    # Filter type
    if selected_type:
        search_sql += " AND type = ?"
        parameters.append(selected_type)
    if selected_year:
        search_sql += " AND released_year = ?"
        parameters.append(selected_year)
    search_sql += " ORDER BY resources_id"
    re_cursor.execute(search_sql, parameters)
    resources = re_cursor.fetchall()
    conre.close()
    return render_template(
        "all_resources.html", resources=resources, types=types, years=years, selected_type=selected_type, selected_year=selected_year
        )

@app.route("/resources/<int:resource_id>", methods=['GET'])
def resources(resource_id):
    conre = sqlite3.connect('database/database.db')
    re_cursor = conre.cursor()
    re_cursor.execute("SELECT resources_id, resources_name, path, type, author, from_link, released_year FROM resources WHERE resources_id=?",
                      (resource_id,)
    )
    resource = re_cursor.fetchone()
    conre.close()
    return render_template(
        "resources.html",
        resource=resource,
    )

if __name__ == "__main__":
    '''if t'''
    app.run(debug=True, port=1234)
