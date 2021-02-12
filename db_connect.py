import configparser
import pymysql.cursors
config=configparser.ConfigParser()
config.read('./config.ini')
host=config['default']['MYSQL_HOST']
user=config['default']['MYSQL_USER']
password=config['default']['MYSQL_PASSWORD']
db=config['default']['MYSQL_DB']

def Connection():
    connection = pymysql.connect(host=host, user= user,password= password,db= db,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor) 
    return connection

def Register(name,user_name,password):
    try:
        sql = "INSERT INTO `twt_dash` (`name`,`username`, `password`) VALUES (%s, %s, %s)"
        connection=Connection()
        cursor=connection.cursor()
        count=cursor.execute(sql,(name,user_name,password))
        connection.commit()
        print("count",count)
        return count
    except Exception as ex:
        return ex

def Sign_In(user_name):
    try:
        sql = "SELECT `password` FROM `twt_dash` WHERE `username`=%s"
        connection=Connection()
        cursor=connection.cursor()
        cursor.execute(sql, (user_name))
        result = cursor.fetchone()
        print("------->>>>>>>",result)
        return result 
    except Exception as ex:
        print("Exception",ex)
        return ex 
    
    
    

