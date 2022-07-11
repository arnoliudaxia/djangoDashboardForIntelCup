import pymysql
import uuid

dbConfig_remote= {'host': '192.168.1.2',"port":49178, 'user': 'root', 'password': 'sh38', 'db': 'meterDB'}
dbConfig_local= {'host': 'localhost',"port":49178, 'user': 'root', 'password': 'sh38', 'db': 'meterDB'}
dbConfig=dbConfig_remote

db = None

config_db_name="labdbAPI_meter_config"

def configureDB(host:str,port:int,user:str,password:str,db:str):
    global dbConfig
    dbConfig['host']=host
    dbConfig['port']=port
    dbConfig['user']=user
    dbConfig['password']=password
    dbConfig['db']=db
    print(dbConfig)
    return 0

def connectDb()->int :
    global db
    db = pymysql.connect(host=dbConfig['host'],
                         port=dbConfig['port'],
                         user=dbConfig['user'],
                         password=dbConfig['password'],
                         database=dbConfig['db'])

    cursor = db.cursor()
    try:
        cursor.execute("SELECT VERSION()")
        cursor.fetchone()
        print("连接数据库成功")
        return 0
    except:
        print("连接数据库失败")
        raise Exception("Could not connect to database")

def disconnectDb():
    db.close()
    print("关闭数据库成功")

def registerMeter(meterName:str,meterGUID:str=None):
    cursor = db.cursor()
    if meterGUID==None:
        meterGUID=str(uuid.uuid1())
    sql=f"INSERT INTO {config_db_name} (meterGUID, meterName) VALUES ('{meterGUID}', '{meterName}')"
    # sql="INSERT INTO config (meterGUID, meterName, isDigital) VALUES ('78763512-da41-4bca-b95a-2b544126da01', 'testMeter1','0')"
    print(sql)
    try:
       cursor.execute(sql)
       db.commit()
       print("注册成功")
       return meterGUID
    except:
        db.rollback()
        print("注册失败")

def removeMeter(meterGUID:str):
    cursor = db.cursor()
    sql=f"DELETE FROM {config_db_name} WHERE meterGUID='{meterGUID}'"
    print(sql)
    try:
       cursor.execute(sql)
       db.commit()
       print("删除成功")
       return 0
    except:
        db.rollback()
        print("删除失败")

def recordValue(meterGUID:str,value:float,time=None):
    cursor = db.cursor()
    if searchMeter(meterGUID=meterGUID)!=0:
        print("没有在注册表中找到该表！无法记录数据")
        print("如果没有注册过该表，请先注册表")
        print("如果已经注册过该表，注意参数是GUID而不是表名")
    if time==None:
        sql=f"INSERT INTO data (value, timestamp, meterGUID) VALUES ('{value}', CURRENT_TIMESTAMP, '{meterGUID}')"
    else:
        sql=f"INSERT INTO data (value, timestamp, meterGUID) VALUES ('{value}', '{time}', '{meterGUID}')"
    print(sql)
    try:
       cursor.execute(sql)
       db.commit()
       print("记录成功")
       return 0
    except:
        db.rollback()
        print("记录失败")

def searchMeter(meterName:str=None,meterGUID:str=None)->int:
    cursor = db.cursor()
    if meterName==None and meterGUID==None:
        raise Exception("meterName and meterGUID can not be both None")
    if meterName==None:
        sql=f"SELECT * FROM {config_db_name} WHERE meterGUID='{meterGUID}'"
    elif meterGUID==None:
        sql=f"SELECT * FROM {config_db_name} WHERE meterName='{meterName}'"
    else:
        sql=f"SELECT * FROM {config_db_name} WHERE meterName='{meterName}' AND meterGUID='{meterGUID}'"
    print(sql)
    try:
       cursor.execute(sql)
       results=cursor.fetchall()
       print("查询成功")
       for result in results:
           print(f"meterName:{result[1]}\nmeterGUID:{result[0]}\nisDigital:{result[2]}")
       if len(results)==0:
           print("没有找到这个仪表，请检查名称和GUID是否正确")
           print("注册新仪表请使用registerMeter函数")
           return 1
       return 0

    except:
        print("查询失败")
        raise Exception("查询失败")
