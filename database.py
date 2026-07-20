from imports import *

'''link the database and python files'''

account_p_connection = sqlite3.connect(
    "database/account_password.db",
    check_same_thread=False # 检查flask多请求
)

post_recourse_eid_connection = sqlite3.connect(
    "database/post_resources_p_eid.db",
    check_same_thread=False
)
recourse_connection = sqlite3.connect(
    "database/resources.db",
    check_same_thread=False
)

subject_connection = sqlite3.connect(
    "database/subject.db",
    check_same_thread=False
)

unit_connection = sqlite3.connect(
    "database/unit.db",
    check_same_thread=False
)

cursor = account_p_connection.cursor()

pid_cursor = post_recourse_eid_connection.cursor()

re_cursor = recourse_connection.cursor()

sub_cursor= subject_connection.cursor()

unit_cursor = unit_connection.cursor()



# connection = sqlite3.connect(

#     "database/account-password.db",

#     check_same_thread=False

# )

# cursor = connection.cursor()


# retrun 