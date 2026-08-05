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


@app.route("/account_create-assword", methods=['GET', 'POST'])
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
            accountcursor.execute(
                "INSERT INTO accountinfo (accountemail, accountpassword) VALUES(?,?)", 
                (input_name, input_password) 
            )
            
            conaccounts.commit()
            conaccounts.close()
        return render_template('homepage.html')
    return render_template('account_create_password.html')

# @app.route


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



@app.route("/resources", methods=['GET', 'POST'])
def resources():
    if request.method =="POST":
         sub_id = request.form.get("sub_id")
         unit_id = request.form.get("unit_id")
         conre = sqlite3.connect('database/resources.db')
         re_cursor = conre.cursor()
         re_cursor.execute(
              "SELECT resources_id, unit, path, author, from_link FROM resources WHERE sub_id=? AND unit_id=?"
              (sub_id, unit_id)
         )
         resources = conre.fetchall()
         conre.commit()
         conre.close()
    return render_template("resources.html", resources=resources, unit_id=unit_id)



if __name__ == "__main__":
    '''if t'''
    app.run(debug=True, port=1234)
