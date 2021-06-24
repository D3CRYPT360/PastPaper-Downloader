#!/usr/bin/env python3
import requests
import os

current_dir = os.getcwd()

class Downloader:
    def __init__(self, exmBoard, subject, subcode, month, year, ptype, pnum):
        self.exmBoard = exmBoard # IGCSE, O level, A levels
        self.subject = subject # Name of the subject
        self.subcode = subcode # Subject Code
        self.month = month # Paper month on / fm / mj
        self.year = year # year of the paper
        self.ptype = ptype # ms or qp or ir
        self.pnum = pnum # Paper number


    def pdfDown(self):
        global url
        url = (f"https://papers.gceguide.com/{self.exmBoard}/{self.subject.capitalize()} ({str(self.subcode)})/{str(self.year)}/{str(self.subcode)}_{self.month}{self.year[2:]}_{self.ptype}_{self.pnum}.pdf")
        r = requests.get(url)
        if r.status_code != 200:
            raise ConnectionRefusedError("Invalid data passed!")
        else:
            fileName = url.split("/")[6]
            open(f"{current_dir}/{fileName}", "wb").write(r.content)
            return fileName


if __name__ == "__main__":
    print("Welcome to the Past Paper Downloader CLI")
    print()
    
    print("""
    Choose your EXAM BOARD:
    [1] IGCSE
    [2] GCSE
    [3] A level
    """)

    exmBoard = input("> ")

    if exmBoard == "1":
        exmBoard = "IGCSE"

    elif exmBoard == "2":
        exmBoard = "O Levels"

    elif exmBoard == "3":
        exmBoard = "A levels"

    else:
        print("Option not available! Exiting.....")
        exit(1)

    print("Enter the name of the subject (please enter the full form :3)")

    subject = input("> ")

    print(f"Enter the syllabus code for {exmBoard} {subject.upper()}")

    subcode = input("> ")

    print("""
    Choose the exam session:

    [1] February / March
    [2] May / June
    [3] October / November
    """)

    month = input("> ")

    if month == "1":
        month = "m"

    elif month == "2":
        month = "s"
    
    elif month == "3":
        month = "w"

    else:
        print("Option not available! Exiting.....")
        exit(1)

    print("Enter the year of the paper you want")

    year = input("> ")

    if len(year) > 4 or len(year) < 4:
        print("Invalid Year passed! Exiting..")
        exit(1)

    print("""
    Choose the paper type:

    [1] Marking Scheme
    [2] Question Paper
    [3] Insert
    """)

    ptype = input("> ")

    if ptype == "1":
        ptype = "ms"

    elif ptype == "2":
        ptype = "qp"
    
    elif ptype == "3":
        ptype = "ir"

    print("Enter the paper number eg: 43")

    pnum = input("> ")

    down = Downloader(exmBoard=exmBoard, subject=subject, subcode=subcode, month=month, year=year, ptype=ptype, pnum=pnum)
    down.pdfDown()

    while True:

        if ptype == "ms":
            print("Would you like to download the Question Paper or the Insert for this paper aswell? [y/n]")
            choice = input("> ")
            if choice.lower() == "y":
                print("""
                Choose the paper type:

                [1] Question Paper
                [2] Insert
                [3] Both
                """)

                opt = input("> ")
                if opt == "1":
                    Downloader(exmBoard=exmBoard, subject=subject, subcode=subcode, month=month, year=year, ptype="qp", pnum=pnum).pdfDown()

                elif opt == "2":
                    Downloader(exmBoard=exmBoard, subject=subject, subcode=subcode, month=month, year=year, ptype="ir", pnum=pnum).pdfDown()

                elif opt == "3":
                    # Probably a better way to do this? threading maybe. will check on that later
                    Downloader(exmBoard=exmBoard, subject=subject, subcode=subcode, month=month, year=year, ptype="qp", pnum=pnum).pdfDown()
                    Downloader(exmBoard=exmBoard, subject=subject, subcode=subcode, month=month, year=year, ptype="ir", pnum=pnum).pdfDown()
                    

                else:
                    print("Option not available! Exiting...")
                    exit(1)

            else:
                print("Alright, Exiting.....")
                exit(1)


        elif ptype == "qp":
            print("Would you like to download the Marking Scheme or the Insert for this paper aswell? [y/n]")
            choice = input("> ")

            if choice.lower() == "y":
                print("""
                Choose the paper type:

                [1] Marking Scheme
                [2] Insert
                [3] Both
                """)

                opt = input("> ")
                if opt == "1":
                    Downloader(exmBoard=exmBoard, subject=subject, subcode=subcode, month=month, year=year, ptype="ms", pnum=pnum).pdfDown()
                    
                elif opt == "2":
                    Downloader(exmBoard=exmBoard, subject=subject, subcode=subcode, month=month, year=year, ptype="ir", pnum=pnum).pdfDown()

                elif opt == "3":
                    # Probably a better way to do this? threading maybe. will check on that later
                    Downloader(exmBoard=exmBoard, subject=subject, subcode=subcode, month=month, year=year, ptype="ms", pnum=pnum).pdfDown()
                    Downloader(exmBoard=exmBoard, subject=subject, subcode=subcode, month=month, year=year, ptype="ir", pnum=pnum).pdfDown()
                
                else:
                    print("Option not available! Exiting...")
                    exit(1)

        elif ptype == "ir":
            print("Would you like to download the Question Paper or the Marking Scheme for this paper aswell? [y/n]")
            choice = input("> ")

            if choice.lower() == "y":
                print("""
                Choose the paper type:

                [1] Question Paper
                [2] Marking Scheme
                [3] Both
                """)

                opt = input("> ")
                if opt == "1":
                    Downloader(exmBoard=exmBoard, subject=subject, subcode=subcode, month=month, year=year, ptype="qp", pnum=pnum).pdfDown()

                elif opt == "2":
                    Downloader(exmBoard=exmBoard, subject=subject, subcode=subcode, month=month, year=year, ptype="ms", pnum=pnum).pdfDown()
                    
                elif opt == "3":
                    # Probably a better way to do this? threading maybe. will check on that later
                    Downloader(exmBoard=exmBoard, subject=subject, subcode=subcode, month=month, year=year, ptype="qp", pnum=pnum).pdfDown()
                    Downloader(exmBoard=exmBoard, subject=subject, subcode=subcode, month=month, year=year, ptype="ms", pnum=pnum).pdfDown()           
                    
                else:
                    print("Option not available! Exiting...")
                    exit(1)

        else:
            print("Alright, Exiting.....")
            exit(1)