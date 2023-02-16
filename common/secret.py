from enum import Enum


class dbconfig(Enum) :
    drivername = "mysql+pymysql"
    port = "3306"
    host = "database-saesam.code5hhx9e0s.ap-northeast-2.rds.amazonaws.com"
    user = "admin"
    password = "00000000"
    charset = "utf8"