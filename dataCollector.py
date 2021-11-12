import json
import os
from time import sleep
import datetime
import os

def convertFromAllMinutes(mins):
    hr=0
    if(mins>=60):
        hr=mins//60
    mins=mins%60
    return (hr,mins)

def collectData():
    data=None
    if "tracker.json" in os.listdir():
        with open("tracker.json",'r') as f:
            data = json.load(f)
    return data

def clear():
    if os.name=='nt':
        _=os.system('cls')
    else:
        _=os.system('clear')

while True:
    clear()
    stats=collectData()
    totalTimeUsed=0
    usage = None
    print("App will count seprete time for apps which are getting used at same time")
    ch=input("enter choice\n1.today's stat\n2.prev report\n3.exit \n")
    try:
        ch=int(ch)
    except:
        ch=4
    if(ch==1):
        dataFound=False
        for stat in stats['data']:
            if(stat['date']==str(datetime.date.today())):
                usage=stat
                dataFound=True
                break
        else:
            print("main.py not initialized today")
            anyKey = input("Enter any key to continue ")
            continue

        if(usage['foreground_apps']==None):
            print("No app record found")
            continue
        else:
            print("Date :",usage['date'])
            totalTimeUsed=0
            for app,time in usage['foreground_apps'].items():
                mins=int( time[:-3])
                totalTimeUsed+=mins
                print(app,":",mins,"mins")
            print("Total time :", totalTimeUsed)
            # converting total min to hrs and mins
            (totalhr,totalmin)=convertFromAllMinutes(totalTimeUsed)
            print("\nTotal time:")
            if(totalhr!=0):
                if(totalhr>1):
                    print(str(totalhr),"hrs")
                else:
                    print(str(totalhr),'hr')
            if (totalmin != 0):
                if (totalmin > 1):
                    print(str(totalmin), "mins")
                else:
                    print(str(totalmin), 'min')

    elif(ch==2):
        date=input("enter date in format (yyyy-mm-dd)\n").strip()
        dataFound=False
        for stat in stats['data']:
            if(stat['date']==date):
                usage=stat
                dataFound=True
                break
        else:
            print(f'data not found for date = {date}')
            anyKey=input("Enter any key to continue ")
            continue

        if (usage['foreground_apps'] == None):
            print("No app record found")
            anyKey = input("Enter any key to continue ")
            continue
        else:
            print("Date :", usage['date'])
            for app, time in usage['foreground_apps'].items():
                mins = int(time[:-3])
                totalTimeUsed += mins
                print(app, mins)
            print("Total time :", totalTimeUsed)

            #converting total min to hrs and mins
            (totalhr, totalmin) = convertFromAllMinutes(totalTimeUsed)
            print("\nTotal time:")
            if (totalhr != 0):
                if (totalhr > 1):
                    print(str(totalhr), "hrs")
                else:
                    print(str(totalhr), 'hr')
            if (totalmin != 0):
                if (totalmin > 1):
                    print(str(totalmin), "mins")
                else:
                    print(str(totalmin), 'min')
    elif(ch==3):
        break
    else:
        print("Wrong Input")
    next=input("enter any key to continue")