import pandas as pd
import os
from datetime import date, timedelta
from connect import connect

conn  = connect()
cursor = conn.cursor()


def equityDB(equityLoc):
    df = pd.read_csv(equityLoc)

    columns = list(df.columns)
    columns[0] = "ID"
    columns = [i.strip() for i in columns]
    dtypes = list(df.dtypes)

    for i in range(len(dtypes)):
        if dtypes[i]=="int64":
            dtypes[i]="INT"
        else:
            dtypes[i]="VARCHAR(255)"

    cond = ["NOT NULL", "NOT NULL", "NOT NULL", "NOT NULL", "NOT NULL", "NOT NULL", "NOT NULL", "NOT NULL", "NOT NULL"]
    df.columns=columns

    sql="CREATE TABLE `EQUITY` ("
    for i in range(len(columns)):
        if i:
            sql=sql+', '
        str = "`{}` {} {}".format(columns[i],dtypes[i],cond[i])
        sql=sql+str
    sql=sql+")  ENGINE = InnoDB;"
    cursor.execute(sql)

    for ind in df.index:
        lst=[]
        
        for col in columns:
            lst.append(df[col][ind])
        
        query = """INSERT INTO `equity` (`ID`, `SYMBOL`, `NAME OF COMPANY`, `SERIES`, `DATE OF LISTING`, `PAID UP VALUE`, `MARKET LOT`, `ISIN NUMBER`, `FACE VALUE`) VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}");""".format(*lst)
        cursor.execute(query)
        conn.commit()


def bhavDB(bhavLoc, dbName):
    df = pd.read_csv(bhavLoc)

    columns = list(df.columns)
    columns = [i.strip() for i in columns]
    dtypes = list(df.dtypes)
    for i in range(len(dtypes)):
        if dtypes[i]=="int64":
            dtypes[i]="INT"
        else:
            dtypes[i]="VARCHAR(255)"
    cond = ["NOT NULL"]*len(dtypes)

    sql="CREATE TABLE `{}` (".format(dbName)
    for i in range(len(columns)):
        if i:
            sql=sql+', '
        str = "`{}` {} {}".format(columns[i],dtypes[i],cond[i])
        sql=sql+str
    sql=sql+")  ENGINE = InnoDB;"
    cursor.execute(sql)

    for ind in df.index:
        lst=[]
        
        for col in columns:
            lst.append(df[col][ind])

        query = """INSERT INTO `{}` (`SYMBOL`, `SERIES`, `OPEN`, `HIGH`, `LOW`, `CLOSE`, `LAST`, `PREVCLOSE`, `TOTTRDQTY`, `TOTTRDVAL`, `TIMESTAMP`, `TOTALTRADES`, `ISIN`, `Unnamed: 13`) VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}");""".format(dbName,*lst)

        cursor.execute(query)
        conn.commit()




def getFileName(date):
    MON = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
           "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    year = date.year
    month = date.month
    date = str(date.day)

    if len(date) == 1:
        date = "0"+date

    dbName =  "cm{}{}{}bhav".format(date, MON[month-1], year)
    file =  "cm{}{}{}bhav.csv".format(date, MON[month-1], year)
    return (dbName,file)


equityDB(os.path.join(os.getcwd(),"tmp","equity",'EQUITY_L.csv'))

for i in range(0, 31):
    dateNow = (date.today()-timedelta(days=i))
    (dbName,file) = getFileName(dateNow)
    bhavLoc = os.path.join(os.getcwd(),"tmp","bhavcopy",file)
    
    if os.path.exists(bhavLoc)==False:
        continue
    
    bhavDB(bhavLoc, dbName)