#!/usr/bin/env python3
import requests
import os 

current_dir = os.getcwd()
# ["0620", "w20", "qp", "12", "pdf"]

validPapers = [11,12,13,21,22,23,41,42,43,51,52,53,61,62,63]
validPtypes = ["qp", "ms"]


def downloader(exmType, subject, subcode, month, year, ptype, pnum):

    """
    exmType -> Exam type IGCSE, O Level, A levels

    subject -> Name of subject

    subcode -> Subject Code

    month -> on paper or fm paper or mj paper

    year -> year of the paper

    ptype -> ms or qp

    pnum -> paper number
    """
    
    url = (f"https://papers.gceguide.com/{exmType}/{subject.capitalize()} ({str(subcode)})/{str(year)}/{str(subcode)}_{month}{year[2:]}_{ptype}_{pnum}.pdf")
    print(url)
    r = requests.get(url)
    if r.status_code != 200:
        return "something went wrong try again"
    else:
        fileName = url.split("/")[6]
        open(f"{current_dir}/{fileName}", "wb").write(r.content)


if __name__ == "__main__":
    print("Welcome to the Past Paper Downloader CLI")
    print()
    while True:
        while True:
            exmType = input("Please enter the exam type of the paper you want! (supported): IGCSE, O Levels, A Levels -> ")
            print()
            if exmType.lower() == "igcse":
                exmType = "IGCSE"
                break
            elif exmType.lower() == "o levels":
                exmType = "O Levels"
                break
            elif exmType.lower() == "a levels":
                exmType = "A Levels"
                break
            else:
                print("Invalid exam type selected! Try again")
                print()

        subject = input("So what subject of {} exam are you looking for? -> ".format(exmType.capitalize()))
        print()

        while True:
            subcode = input("Awesome! what's the subject code of {} {}? -> ".format(exmType.capitalize(), subject.capitalize()))
            print()
            if len(str(subcode)) > 4 or len(str(subcode)) < 4:
                print("Invalid subject code passed, Try again!")
                print()
            else:
                break
        while True:
            year = input("Wonderful! Now what's the year of the {} {} paper you are looking for? -> ".format(exmType.capitalize(), subject.capitalize()))
            print()
            if len(str(year)) > 4 or len(str(year)) < 4:
                print("Invalid year passed try again!")
                print()
            else:
                break

        while True:
            month = input("What month's paper are you looking for eg: o/n or on? -> " )
            print()
            if month.lower() == "fm" or month.lower() == "f/m":
                month = "m"
                break
            elif month.lower() == "mj" or month.lower() == "m/j":
                month = "s"
                break
            elif month.lower() == "on" or month.lower() == "o/n":
                month = "w"
                break
            else:
                print("Invalid month passed!, try again!")
                
        while True:
            ptype = input("Are you looking for a Marking Scheme (ms) or a Question Paper (qp)? -> ")
            print()
            if ptype.lower() not in validPtypes:
                print("Invalid Paper Type passed!, Try again!")
                print()
            else:
                break 

        while True:
            pnum = input("Final step, What is the paper number eg: 62, 33? -> ")
            print()
            if int(pnum) not in validPapers:
                print("Invalid Paper number passed, Try again!")
            else:
                break

        down = downloader(exmType, subject, subcode, month, year, ptype, pnum)
        if down == "something went wrong try again":
            print("something went wrong try again")
        else:
            print("Paper Downloaded! Thanks for using this tool, hope it saved you time :)")
            print("exiting...")
            exit(1)