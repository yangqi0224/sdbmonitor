import pymysql


def get_conn(user_name, user_pwd, addr, port):
    conn = pymysql.connect(host='addr', user=user_name, password=user_pwd, port=port)
    return conn;

