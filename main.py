import subprocess
import json
from time import sleep
import os
import datetime
import win32gui, win32process, psutil

today=datetime.date.today()

print(os.getcwd())

template={
        'data':
            [
                {
                    "date":str(datetime.date.today()),
                    "foreground_apps":{},
                    "background_apps":{}
                }
            ]
    }

def get_focused_app():
    try:
        pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
        return(psutil.Process(pid[-1]).name())
    except:
        pass


def get_minimized_apps():
    minimized_apps=[]
    cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Description'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in proc.stdout:
        if line.rstrip():
            minimized_apps.append(line.decode().rstrip().lower())
    return minimized_apps[2:]

def add_template():
    with open("tracker.json",'w') as f:
            json.dump(template, f)
            f.close()
    print("added template")

def check_file():
    try:
        with open("tracker.json",'r') as f:
            data=json.load(f)
            data=data['data']
    except:
        print("issue in file..rewriting file")
        add_template()
        print("file rewrited..")


def create_file():
        with open("tracker.json",'w') as f:
            f.close()
        add_template()


if "tracker.json" not in os.listdir():
    print("adding file")
    create_file()
    print("file created.")


while True:
    check_file()
    prev_app=get_focused_app().lower()    
    sleep(60)
    todayFound=False
    today=datetime.date.today()
    currTime=datetime.datetime.now()
    with open("tracker.json") as f:
        data=json.load(f)
        data=data['data']

    curr_app=get_focused_app().lower()
    minimized_apps=get_minimized_apps()
    if(curr_app==prev_app and curr_app.lower()!='lockapp.exe' and curr_app and curr_app.lower()!='lockapp'):
        curr_app=curr_app[:-4]
        for statDaily in data:
            if(statDaily['date']==str(today)):
                todayFound=True
                prevUsedTime=statDaily['foreground_apps'].get(curr_app,0)#if curr app is not there then get value as 0
                if prevUsedTime!=0:
                    minute=int( prevUsedTime[0:prevUsedTime.find('m')] )
                else:
                    minute=0
                statDaily['foreground_apps'][curr_app]=(str(minute+1)+"min")
                print(currTime,'->',(minute+1),curr_app.lower())
                
        #if date not found
        if(todayFound == False):
            print("today's date not found")
            #adding dictionary for today's record
            todayStat={'date':str(today),'foreground_apps':{},'background_apps':{}}
            data.append(todayStat)
            print("added today's date")

    if curr_app.lower()!='lockapp.exe' and curr_app!='lockapp':
        minimized_apps=get_minimized_apps()
        for i in minimized_apps:
            if(curr_app in i):
                #removing first occurence of app in all apps list with name containing word of focused app
                minimized_apps.remove(i)
                break
        #got minimized apps without current app which is in focus
        #print(f"{today} minimized apps",minimized_apps)
        for statDaily in data:
                if(statDaily['date']==str(today)):
                    for each_app in minimized_apps:
                        prevUsedTime=statDaily['background_apps'].get(each_app,0)
                        if prevUsedTime!=0:
                            minute=int( prevUsedTime[0:prevUsedTime.find('m')] )
                        else:
                            minute=0
                        statDaily['background_apps'][each_app]=(str(minute+1)+"min")
                    break


    #rewriting json file
    newData=dict()
    newData['data']=data
    with open("tracker.json",'w') as f:
        json.dump(newData,f)
        f.close()
