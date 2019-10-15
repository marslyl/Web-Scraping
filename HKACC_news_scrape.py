import requests
from bs4 import BeautifulSoup
import os

newsLinkStr = "http://www.aircadets.org.hk/web/news.php"

print("Scraping from HKACC news site...")
r = requests.get(newsLinkStr, timeout = 30)
s = BeautifulSoup(r.text, "lxml")

rawList = s.find_all(["a","b"])

head = 21       #20 is Home and 21 is the first date
for listNum in range(len(rawList)):
    if rawList[listNum].string == "Next":
        tail = listNum

cutList = rawList[head:tail]

urlHead = "http://www.aircadets.org.hk/web/"
outList = []
for item in cutList:
    if item.name == "b":
        dateStr = item.string
    else:
        outList.append([item.string, urlHead + str(item.get("href")), dateStr])

outList.reverse()
dateTemp = ""

logFileStr = r"hkacc_news_scraping_log.txt"
try:
    f = open(logFileStr, "r")
    #Check if all-updated
    lineList = f.readlines()
    try:
        latestNews = [lineList[-2][1:-1], lineList[-1][2:-1]]
        for item in reversed(lineList):
            if "\t" not in item:
                dateTemp = item[:-1]
                latestNews.append(dateTemp)
                break

        if latestNews in outList:
            xHead = outList.index(latestNews)
            outList = outList[xHead + 1:]

    except IndexError:
        print("Local log is empty.")

    f.close()

except OSError:
    print("No existing local log.")

if outList == []:
    print("No new update available.")
else:
    print("The followings are newly available:")

#write new events
f = open(logFileStr, "a")

for item in outList:
    if item[2] != dateTemp:
        dateTemp = item[2]
        f.write(dateTemp + "\n")
        print(dateTemp + "\n")
    f.write("\t" + item[0] + "\n" +\
            "\t\t" + item[1] + "\n")
    print("\t" + item[0] + "\n" +\
            "\t\t" + item[1] + "\n")
f.close()

if input("Do you want to read the log (Y/N)? ") in ["Y", "y"]:
    os.startfile(logFileStr, "open")
