from imports import *

app.secret_key = "awdawdawd"
@app.route("/", methods=['GET', 'POST'])
def index():
        if request.form.get("submit") =="next":
             return render_template("account_create.html")
        return render_template("index.html")


@app.route("/account_create", methods=['GET', 'POST'])
def account_create():
    if "back" in request.form:
            return redirect(url_for("index"))
    if request.method == "POST":
        if 'account_name' in request.form:
            input_name = request.form.get('account_name')
            session["input_name"] = input_name  # 把变量 email 的值保存起来，并命名为 "email"，以后这个用户访问其他页面时都可以取出来
        if not input_name or ".com" not in input_name:
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
            accountcursor = conaccounts.cursor()
            accountcursor.execute("SELECT * FROM accountinfo WHERE accountemail=?",
                                  (input_name,)
                                  )
            user = accountcursor.fetchone()
            if user:
                conaccounts.close()
                return render_template("account_create_password.html" 
                                       ,create_password_error="This email already exists, pls go back"
                                       )
            accountcursor.execute(
                "INSERT INTO accountinfo (accountemail, accountpassword) VALUES(?,?)", 
                (input_name, input_password) 
            )

            
            
            conaccounts.commit()
            conaccounts.close()
        return render_template('homepage.html')
    return render_template('account_create_password.html')

# @app.route

@app.route("/account", methods=['GET', 'POST'])
def account():
     if request.method == "POST":
        action = request.form.get("action")
        conaccounts = sqlite3.connect("database/account_password.db")
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
             return render_template("account.html", report_message="Wrong email or password")
        # Change Password
            
        elif action == "change_password":
            email = session.get("email")
            if not email:
                conaccounts.close()
                return render_template("account.html", report_message="Pls login first")
            old_password = request.form.get("old_password")
            new_password = request.form.get("new_password")
            accountcursor.execute(" SELECT * FROM accountinfo WHERE accountemail=? AND accountpassword=?", 
                (email, old_password)
            )
            user = accountcursor.fetchone()
            if not user:
                conaccounts.close()
                return render_template("account.html", report_message="Old password is incorrect")
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
                return render_template("account.html", report_message="Wrong email or password")
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
            consearch = sqlite3.connect('database/resources.db')
            searchcursor = consearch.cursor()
            query_search = f"%{search_input}%" # 什么意思
            searchcursor.execute(
                "SELECT unit, subject, resources_name FROM resources WHERE unit LIKE ? OR subject LIKE ? OR resources_name LIKE ?",
                (query_search, query_search, query_search)
            )
            search_results = searchcursor.fetchall()
            return render_template("search_results.html", results = search_results, keywords = search_input)
    return render_template("homepage.html")



@app.route("/search_results", methods=['GET', 'POST'])
def search_results():
    # if request.method =="POST":
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
    consub_id = sqlite3.connect('database/unit.db')
    unit_cursor = consub_id.cursor()
    unit_cursor.execute(
         "SELECT unit_id, unit FROM unit WHERE sub_id=?",
        (sub_id,)
    )# SELECT unit_id, unit 不加括号
    units = unit_cursor.fetchall() # 将从database中搜索到的数据取出，并变成python列表
    return render_template("subjectpick_unity.html", units = units, sub_id = sub_id)


@app.route("/resources_list/<int:unit_id>", methods=['GET', 'POST'])
def resources_list(unit_id):
    conre_list = sqlite3.connect('database/resources.db')
    re_cursor = conre_list.cursor()
    re_cursor.execute(
         "SELECT resources_id, resources_name, author FROM resources WHERE unit_id = ?",
         (unit_id,)
)
    resources = re_cursor.fetchall()
    conre_list.close()
    return render_template("resources_list.html", resources = resources, unit_id = unit_id)






@app.route("/resources/<int:sub_id>/<int:unit_id>", methods=['GET'])
def resources(sub_id, unit_id):

    conre = sqlite3.connect('database/resources.db')
    re_cursor = conre.cursor()

    re_cursor.execute(
        """
        SELECT resources_id, resources_name, path, type, author, from_link
        FROM resources
        WHERE sub_id=? AND unit_id=?
        """,
        (sub_id, unit_id)
    )

    resources = re_cursor.fetchall()

    conre.close()

    return render_template(
        "resources.html",
        resources=resources,
        sub_id=sub_id,
        unit_id=unit_id
    )

@app.route("/all_resources", methods=['GET', 'POST'])
def all_resources():
    selected_type = request.args.get("type", "")
    selected_year = request.args.get("released_year", "")
    conre = sqlite3.connect("database/resources.db")
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
        "all_resources.html",
        resources=resources,
        types=types,
        years=years,
        selected_type=selected_type,
        selected_year=selected_year
        )


@app.route("/detail_resource/<int:resources_id>")
def resource(resources_id):

    conre = sqlite3.connect("database/resources.db")
    re_cursor = conre.cursor()

    re_cursor.execute(
        """
        SELECT
            resources_id,
            subject,
            unit,
            resources_name,
            path,
            type,
            author,
            from_link,
            released_year
        FROM resources
        WHERE resources_id=?
        """,
        (resources_id,)
    )

    resource_data = re_cursor.fetchone()

    conre.close()

    if resource_data is None:
        return "Resource not found", 404

    return render_template(
        "resource.html",
        resource=resource_data
    )

# @app.route("/resources", methods=['GET', 'POST'])
# def resources():
#     if request.method =="POST":
#          sub_id = request.form.get("sub_id")
#          unit_id = request.form.get("unit_id")
#          conre = sqlite3.connect('database/resources.db')
#          re_cursor = conre.cursor()
#          re_cursor.execute(
#               "SELECT resources_id, unit, path, author, from_link FROM resources WHERE sub_id=? AND unit_id=?",
#               (sub_id, unit_id)
#          )
#          resources = conre.fetchall()
#          conre.commit()
#          conre.close()
#     return render_template("resources.html", resources=resources, unit_id=unit_id)



if __name__ == "__main__":
    '''if t'''
    app.run(debug=True, port=1234)
