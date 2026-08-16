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

# account creation page
@app.route("/account_create", methods=['GET', 'POST'])
def account_create():
    # check whether the user clicked the back button
    if "back" in request.form:
            return redirect(url_for("index"))
    if request.method == "POST":
        if 'account_name' in request.form:
            input_name = request.form.get('account_name')
            session["input_name"] = input_name  
            # save the vulme email，and name email to "email", take this vulme in next page
        if not input_name:
                # Check whether the user enteredz email address
                return render_template(
                    "account_create.html",
                    create_password_error="Your email address can't be empty"
                )
        # check whether the email has a basic valid format
        if ("@" not in input_name or input_name.startswith("@") or input_name.endswith("@") or "@." in input_name or (".com" not in input_name and ".nz" not in input_name)):
            return render_template(
                "account_create.html",
                create_password_error="You must input a correct email address"
            )
        #move to the password creation page after the email passes 
        return redirect(url_for('account_create_password'))
        # Store the variable before moving to the next page
    return render_template("account_create.html")


@app.route("/account_create-password", methods=['GET', 'POST'])
def account_create_password():
    # back to the previous page if the user clicked the back button
    if "back" in request.form:
         return redirect(url_for("account_create"))
    if request.method == "POST":
        if 'account_password' in request.form:
            # get the input_password by the user
            input_password = request.form.get('account_password')
            #get the ensure_input_password
            ensure_input_password = request.form.get('ensure_account_password')
            # get the email from email saved before
            input_name = session.get("input_name")
            if input_password != ensure_input_password:
                return render_template(
                    "account_create_password.html",
                    create_password_error="Please check your ensure password is same with your password"# error feedback
                    )
            #prevent the user from submitting an empty password or password containing spaces
            if not input_password or not ensure_input_password:
                return render_template(
                    "account_create_password.html",
                    create_password_error="Your password can not be empty"
                )
             # check whether the password is at least 8 characters long
            if len(input_password) < 8:
                return render_template(
                    "account_create_password.html",
                    create_password_error="Your password must be at least 8 characters"
                )
            # check user using letters
            if not re.search(r"[A-Za-z]", input_password):
                return render_template(
                    "account_create_password.html",
                    create_password_error="Your password must contain letters"
                )
            # check user using number
            if not re.search(r"[0-9]", input_password):
                return render_template(
                    "account_create_password.html",
                    create_password_error="Your password must contain numbers"
                )
            # link the database file
            conaccounts = sqlite3.connect('database/database.db')
            # create a cursor to execute sql commands
            accountcursor = conaccounts.cursor()
            # search input_name put in accountinfo
            accountcursor.execute("SELECT * FROM accountinfo WHERE accountemail=?",
                                  (input_name,)
                                  )
            # get matching account, if no account, reture none
            user = accountcursor.fetchone()
            # check user using same email
            if user:
                conaccounts.close()
                return render_template("account_create_password.html" 
                                       ,create_password_error="This email already exists, please go back"
                                       )
            # input input_name and input_password into accountemail and accountpassword
            accountcursor.execute(
                "INSERT INTO accountinfo (accountemail, accountpassword) VALUES(?,?)", 
                (input_name, input_password) 
            )
            # save changes in database
            conaccounts.commit()
            # close database
            conaccounts.close()
        # moev to homepage
        return render_template('homepage.html')
    return render_template('account_create_password.html')

@app.route("/account", methods=['GET', 'POST'])
def account():
     if request.method == "POST":
        # get action form user
        action = request.form.get("action")
        # link the database file
        conaccounts = sqlite3.connect("database/database.db")
        accountcursor = conaccounts.cursor()
        #login
        if action =="login":
             # get email from user
             email = request.form.get("login_email")
             # get password
             password = request.form.get("login_password")
             # input email and password vlume into accountemail and accountpassword
             accountcursor.execute(
                  "SELECT * FROM accountinfo WHERE accountemail=? AND accountpassword=?",
                  (email, password)
             )
             # get the matching account from the database
             user = accountcursor.fetchone()
             if user:
                # save email
                session["email"] = email
                # close database
                conaccounts.close()
                # remaind user 
                return render_template("account.html", report_message="Login successful")
             conaccounts.close()
             return render_template("account.html", report_message="Your email or password is incorrect")

        # Change Password
        elif action == "change_password":
            # get email form session in last part
            email = session.get("email")
            # if not, remaind user login 
            if not email:
                conaccounts.close()
                return render_template("account.html", report_message="Please login your account first")
            # get old_password
            old_password = request.form.get("old_password")
            # get new_password
            new_password = request.form.get("new_password")
            # check the new_password and old_password between accountemail and accountpassword
            accountcursor.execute(" SELECT * FROM accountinfo WHERE accountemail=? AND accountpassword=?", 
                (email, old_password)
            )
            #get matching account
            user = accountcursor.fetchone()
            #stop password change if the original password is incorrect
            if not user:
                conaccounts.close()
                return render_template("account.html", report_message="Your original password is incorrect")
            # check user's password is more then 8
            if len(new_password) < 8:
                return render_template("account.html",
                                       report_message="Your password must be at least 8 characters"
                                       )
            # check user using letters for password
            if not re.search(r"[A-Za-z]", new_password):
                return render_template("account.html",
                                       report_message="Your password must contain letters"
                                       )
            # check user using number for password
            if not re.search(r"[0-9]", new_password):
                return render_template("account.html",
                                       report_message="Your password must contain numbers"
                                       )
            # update the password for the logged-in user's account
            accountcursor.execute("UPDATE accountinfo SET accountpassword=? WHERE accountemail=?", 
                                  (new_password, email)
                )
            # Save the password change to the database
            conaccounts.commit()
            # Close the database connection
            conaccounts.close()
            return render_template("account.html", report_message="Password changed successfully")
        # Delete Account
        elif action == "delete_account":
            # get the information of ensure_email
            email = request.form.get("ensure_email")
            # get the information of delete_password
            password = request.form.get("delete_password")
            # Check the provided emial and password match an existing account
            accountcursor.execute( "SELECT * FROM accountinfo WHERE accountemail=? AND accountpassword=?", 
                                  (email, password)
                                  )
            # get the matching account
            user = accountcursor.fetchone()
            # the password not correct
            if not user:
                # close the database
                conaccounts.close()
                # remaind user
                return render_template("account.html", report_message="Your email or password is incorrect")
            accountcursor.execute("DELETE FROM accountinfo WHERE accountemail=?",
                                  (email,)
                                  )
            # save data changed
            conaccounts.commit()
            # clear information that saved
            session.clear()
            # close databse
            conaccounts.close()
            # give user feedback
            return render_template("account.html", report_message="Account deleted.")
        return render_template('account.html')
     return render_template('account.html')




@app.route("/homepage", methods=['GET', 'POST'])
def homepage():
    if request.method =="POST":
        # check whether the search form was submitted
        if 'Searchbar_q' in request.form:
            # get the imformation of Searchbar_q
            search_input = request.form.get('Searchbar_q')
            # ensure user not search empty 
            if not search_input or not search_input.strip():
                return render_template(
                    "search_results.html",
                    error_resource_text="Your search bar can't be empty or space"
                )
            # link database 
            consearch = sqlite3.connect('database/database.db')
            searchcursor = consearch.cursor()
            #add % before and after the search input to allow partial matches
            query_search = f"%{search_input}%"
            searchcursor.execute(
                # search the unit, subject, and resource name columns
                "SELECT resources_id, unit, subject, resources_name FROM resources WHERE unit LIKE ? OR subject LIKE ? OR resources_name LIKE ?",
                (query_search, query_search, query_search)
            )
             #get all matching resources from the database
            search_results = searchcursor.fetchall()
            # display search_results page and show keyword 
            return render_template("search_results.html", results = search_results, keywords = search_input)
    return render_template("homepage.html")



@app.route("/search_results", methods=['GET', 'POST'])
def search_results():
    # display the search results page
    return render_template("search_results.html")




@app.route("/subjectpic/", methods=['GET','POST']) 
def subjectpick():
    if request.method == "POST":
        if 'subject' in request.form:
            # get the subject of the selected subject
            sub_id = request.form.get('subject')
            # redirect to the unit selection page using the selected subject id
            return redirect(url_for("unit", sub_id = sub_id))
        return render_template("subjectpick_unity.html")
    return render_template("subjectpick_main.html")




@app.route("/unit/<int:sub_id>", methods=['GET','POST'])
def unit(sub_id):#int:sub_id needs sub_id
    # connect to the database
    consub_id = sqlite3.connect('database/database.db')
    unit_cursor = consub_id.cursor()
    # find the right selected subject
    unit_cursor.execute(
         "SELECT unit_id, unit FROM unit WHERE sub_id=?",
        (sub_id,)
    )
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
