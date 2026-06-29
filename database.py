from imports import *

'''link the database and python files'''

account_p_connection = sqlite3.connect("database/account_password.db")

post_recourse_eid_connection = sqlite3.connect(
    "database/post_resources_p_eid.db"
)
recourse_eid_connection = sqlite3.connect(
    "database/resources_eid.db"
)

cursor = account_p_connection.sursor()



# connection = sqlite3.connect(

#     "database/account-password.db",

#     check_same_thread=False

# )

# cursor = connection.cursor()


# retrun 