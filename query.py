from connect import connect
import os
from datetime import date, timedelta
import csv

conn = connect()
cursor = conn.cursor()


def getFileName(date):
    MON = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
           "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    year = date.year
    month = date.month
    date = str(date.day)

    if len(date) == 1:
        date = "0"+date

    dbName = "cm{}{}{}bhav".format(date, MON[month-1], year)
    filetxt = "cm{}{}{}bhav.txt".format(date, MON[month-1], year)
    filecsv = "cm{}{}{}bhav.csv".format(date, MON[month-1], year)
    return (dbName, filetxt, filecsv)


def query(db, fileLoc):
    q = """SELECT ISIN, ((close-open)/close)*100 as gain
    FROM {}
    order by gain desc LIMIT 25""".format(db)
    cursor.execute(q)
    myresult = cursor.fetchall()

    with open(fileLoc, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=" ", skipinitialspace=True)
        for x in myresult:
            writer.writerow(x)

def query3(dbNew, dbOld, fileLoc):
    q = """SELECT new.ISIN, ((new.close-old.open)/new.close) gain
    FROM {} new, {} old where new.ISIN = old.ISIN
    order by gain desc LIMIT 25""".format(dbNew, dbOld)

    cursor.execute(q)
    myresult = cursor.fetchall()

    with open(fileLoc, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=" ", skipinitialspace=True)
        for x in myresult:
            writer.writerow(x)

def getNewest():
    for i in range(0, 31):
        dateNow = (date.today()-timedelta(days=i))
        (dbName, filetxt, filecsv) = getFileName(dateNow)
        bhavLoc = os.path.join(os.getcwd(), "tmp", "bhavcopy", filecsv)

        if os.path.exists(bhavLoc) == True:
            return (dbName, filetxt, filecsv)

    return (None, None, None)


def getOldest():
    (_dbName, _filetxt, _filecsv) = (None, None, None)

    for i in range(0, 31):
        dateNow = (date.today()-timedelta(days=i))
        (dbName, filetxt, filecsv) = getFileName(dateNow)
        bhavLoc = os.path.join(os.getcwd(), "tmp", "bhavcopy", filecsv)

        if os.path.exists(bhavLoc) == True:
            (_dbName, _filetxt, _filecsv) = (dbName, filetxt, filecsv)

    return (_dbName, _filetxt, _filecsv)

for i in range(0, 31):
    dateNow = (date.today()-timedelta(days=i))
    (dbName, filetxt, filecsv) = getFileName(dateNow)
    bhavLoc = os.path.join(os.getcwd(), "tmp", "bhavcopy", filecsv)
    queryLoc = os.path.join(os.getcwd(), "tmp", "query", filetxt)

    if os.path.exists(bhavLoc) == False:
        continue
    query(dbName, queryLoc)


(dbNew,*args) = getNewest()
(dbOld,*args) = getOldest()
fileLoc = os.path.join(os.getcwd(),"tmp","query","query3.txt")
query3(dbNew, dbOld, fileLoc)