from datetime import date, timedelta
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from zipfile import ZipFile
import time
import pandas as pd

def downloadFile(url, filename, location):
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory": location}
    chromeOptions.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=chromeOptions)

    driver.get(url)
    time.sleep(3)
    driver.close()

    zipLocation = os.path.join(location, filename)

    with ZipFile(zipLocation, 'r') as zObject:
        zObject.extractall(path=location)

    os.remove(zipLocation)

# security
print("----------------downloading equity.csv ----------------")
df=pd.read_csv("https://archives.nseindia.com/content/equities/EQUITY_L.csv")
df.to_csv("./tmp/equity/EQUITY_L.csv")
print("----------------downloaded equity.csv ----------------")

def getFileName(date):
    MON = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
           "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    year = date.year
    month = date.month
    date = str(date.day)

    if len(date) == 1:
        date = "0"+date

    return "cm{}{}{}bhav.csv.zip".format(date, MON[month-1], year)


def bhavCopyURL(date):
    MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
           "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    year = date.year
    month = date.month
    date = str(date.day)

    if len(date) == 1:
        date = "0"+date

    url = "https://www.nseindia.com/api/reports?archives=%5B%7B%22name%22%3A%22CM%20-%20Bhavcopy(csv)%22%2C%22type%22%3A%22archives%22%2C%22category%22%3A%22capital-market%22%2C%22section%22%3A%22equities%22%7D%5D&date={}-{}-{}&type=equities&mode=single".format(
        date, MON[month-1], year)

    return url


def getLastbhavCopies():
    location = os.path.join(os.getcwd(), "tmp", "bhavcopy")

    for i in range(0, 31):
        dateNow = (date.today()-timedelta(days=i))
        url = bhavCopyURL(dateNow)
        filename = getFileName(dateNow)

        try:
            print("--------- Downloading {} from date {} -------".format(filename,dateNow))
            downloadFile(url,filename,location)
            print("--------- Downloaded {} -------".format(filename))
        except:
            print("Opps {} not found! date {}".format(filename, dateNow))


getLastbhavCopies()
