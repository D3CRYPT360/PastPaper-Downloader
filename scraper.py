#!/usr/bin/env python
import os
import requests
import re
from bs4 import BeautifulSoup
import time 

"""
Contains Modified parts of code taken from 
https://github.com/Dharisd/pastpaper-bot/blob/master/scrp.py (line 23 to 26)
"""
allLinks = {}

def Converter(exmType):

    if exmType.lower() == "gce":
        return "O Levels"
    elif exmType.lower() == "a levels":
        return "A Levels"
    elif exmType.lower() == "igcse":
        return exmType.upper()
    

def scrape(exmType, subject, code, year, ptype, month):
    """
    exmType - > Exam Type eg: IGCSE, O Levels, A Levels

    subject - > Subject eg: chemistry, physics

    code - > Syllabus code eg: 0620 (This is the syllabus code of IGCSE chemistry)

    year - > The year the paper was released 

    ptype - > Paper Types eg: qp (Question Paper), ms (Marking Scheme), gt (Grade Threshold), ir (Information Report), sp (Speciment Paper)

    month - > The exam session month eg: ON or o/n(October November)
    """
    global url
    url = (f"https://papers.gceguide.com/{Converter(exmType)}/{subject.capitalize()} ({str(code)})/{str(year)}")
    r = requests.get(url)
    
    
    html_page = r
    soup = BeautifulSoup(html_page.text, features="html.parser")
    global a_tags
    a_tags = soup.find_all("a", href=re.compile(r'(.pdf)'))
    
    if ptype.lower() == "qp":
        return qp(month)

    elif ptype.lower() == "ms":
        return ms(month)
    

def ms(month):
    global msarr
    msarr = [] # All links with Marking Schemes 
    for tag in a_tags:
        if month.lower() == "fm" or month.lower() == "f/m": # February March -> March Paper
            if tag["href"].split("_")[2] == "ms" and tag["href"].split("_")[1][0] == "m": # ["0620", "m20", "ms", "12", "pdf"]
                msarr.append(tag["href"])

        elif month.lower() == "mj" or month.lower() == "m/j": # May June -> Summer Paper
            if tag["href"].split("_")[2] == "ms" and tag["href"].split("_")[1][0] == "s": # ["0620", "s20", "ms", "12", "pdf"]
                msarr.append(tag["href"])

        elif month.lower() == "on" or month.lower() == "o/n": # October November -> Winter Paper
            if tag["href"].split("_")[2] == "ms" and tag["href"].split("_")[1][0] == "w": # ["0620", "w20", "ms", "12", "pdf"]
                msarr.append(tag["href"])
    
    enumeratedList = [] # To make it more easier to select the array number
    enumeratedDict = {}
    for x in range(len(msarr)):
        enumerated = f"{msarr[x]}" 
        enumeratedList.append(enumerated)
        id = x
        enumeratedDict[id] = enumeratedList[x]
    return enumeratedDict

    

def qp(month):
    global qparr
    qparr = [] # All links with question papers
    for tag in a_tags:
        if month.lower() == "fm" or month.lower() == "f/m": # February March -> March Paper
            if tag["href"].split("_")[2] == "qp" and tag["href"].split("_")[1][0] == "m": # ["0620", "m20", "qp", "12", "pdf"]
                qparr.append(tag["href"])

        elif month.lower() == "mj" or month.lower() == "m/j": # May June -> Summer Paper
            if tag["href"].split("_")[2] == "qp" and tag["href"].split("_")[1][0] == "s": # ["0620", "s20", "qp", "12", "pdf"]
                qparr.append(tag["href"])

        elif month.lower() == "on" or month.lower() == "o/n": # October November -> Winter Paper
            if tag["href"].split("_")[2] == "qp" and tag["href"].split("_")[1][0] == "w": # ["0620", "w20", "qp", "12", "pdf"]
                qparr.append(tag["href"])


    enumeratedList = [] # To make it more easier to select the array number
    enumeratedDict = {}
    for x in range(len(qparr)):
        enumerated = f"{qparr[x]}" 
        enumeratedList.append(enumerated)
        id = x
        enumeratedDict[id] = enumeratedList[x]
    return enumeratedDict

def download(arrayNo):
    link = url + f"/{qparr[int(arrayNo)]}"
    global fileName
    fileName = qparr[int(arrayNo)]
    pdf = requests.get(link)
    open(f"/home/d3crypt360/Desktop/Python/pastpaperdisc/pastdown/{fileName}", "wb").write(pdf.content)


def delete():
    time.sleep(60) # 1 Min because it usually takes 1 minute to download file in slow internet speeds
    os.remove(f"/home/d3crypt360/Desktop/Python/pastpaperdisc/pastdown/{fileName}") # Deletes file
    


  
def fileName():

    return fileName

if __name__ == "__main__":
    test = scrape("igcse", "chemistry", "0620", "2020", "qp", "f/m")


    for t in range(len(test)):  
        print(f"{test[t]}" + "\n") # Print in in new line
    arr = input("Select the number of the paper to download : ")
    download(arr)