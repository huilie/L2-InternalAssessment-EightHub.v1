from imports import *

'''link the database and python files'''

account_p_connection = sqlite3.connect("database/account-password.db")

post-recourse-eid_connection = sqlite3.connect(
    "database/.db"
)
recourse-eid_connection = sqlite3.connect(
    "database/.db"
)

cursor = account_p_connection.sursor()



# connection = sqlite3.connect(

#     "database/account-password.db",

#     check_same_thread=False

# )

# cursor = connection.cursor()


# retrun 