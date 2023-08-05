import time
import webbrowser as web
import pyautogui as pg
import wikipedia
import requests
from bs4 import BeautifulSoup
import platform
import os

last = time.time()
pg.FAILSAFE = False
sleeptm = "None, You can use this function to print the remaining time in seconds."

class CountryCodeException(Exception):
    pass

class CallTimeException(Exception):
    pass

class InternetException(Exception):
    pass

def watch_tutorial():
    """Watch tutorial on how to use this library on YouTube"""
    web.open("https://www.youtube.com/watch?v=Fy7hmZ_YDjQ&lc=z23nj3holprcjb5v4acdp434fbsdojdlsywud4kb3htw03c010c")
    #Previously, it was this video https://www.youtube.com/watch?v=3hUi0qfrWWo&t=3s
    
def showHistory():
    """Prints the information of all last sent messages using this program"""
    file = open("pywhatkit_history.txt","r")
    content = file.read()
    file.close()
    if content == "--------------------":
        content = None
    print(content)

def shutdown(time = 20):
    """Will shutdown the computer in given seconds
For Windows and Linux only"""
    global osname
    osname = platform.system()
    if "window" in osname.lower():
        cont = "shutdown -s -t %s"%time
        os.system(cont)

    elif "linux" in osname.lower():
        cont = "shutdown -h %s"%time
        os.system(cont)

    else:
        raise Warning("This function is for Windows and Linux only, can't execute on %s"%osname)

def cancelShutdown():
    """Will cancel the scheduled shutdown"""
    if "window" in osname.lower():
        cont = "shutdown/a"
        os.system(cont)

    elif "linux" in osname.lower():
        cont = "shutdown -c"
        os.system(cont)

    else:
        raise Warning("This function is for Windows and Linux only, can't execute on: %s"%osname)

def prnt_sleeptm():
    return sleeptm

def check_window():
    web.open("https://www.google.com")
    pg.alert("If the browser's window is not maximised\nMaximise and then close it if you want,\nor sendwhatmsg() function will not work","Pywhatkit")

def sendwhatmsg(phone_no, message, time_hour, time_min, print_waitTime=True):
    '''Sends whatsapp message to a particulal number at given time
Phone number should be in string format not int
***This function will not work if the browser's window is minimised,
first check it by calling 'check_window()' function'''
    if "+" not in phone_no:
        raise CountryCodeException("Country code missing from phone_no")
    timehr = time_hour

    if time_hour == 0:
        time_hour = 24
    callsec = (time_hour*3600)+(time_min*60)
    
    curr = time.localtime()
    currhr = curr.tm_hour
    currmin = curr.tm_min
    currsec = curr.tm_sec

    currtotsec = (currhr*3600)+(currmin*60)+(currsec)
    lefttm = callsec-currtotsec

    if lefttm <= 0:
        lefttm = 86400+lefttm

    if lefttm < 60:
        raise CallTimeException("Call time must be greater than one minute as web.whatsapp.com takes some time to load")
    
    else:
        global sleeptm
        date = "%s:%s:%s"%(curr.tm_mday,curr.tm_mon,curr.tm_year)
        time_write = "%s:%s"%(timehr,time_min)
        file = open("pywhatkit_history.txt","a")
        file.write("\nDate: %s\nTime: %s\nPhone number: %s\nMessage: %s"%(date,time_write,phone_no,message))
        file.write("\n--------------------")
        file.close()
        sleeptm = lefttm-60
        if print_waitTime :
            print(prnt_sleeptm(),"+ 60 seconds left")
        time.sleep(sleeptm)
        web.open('https://web.whatsapp.com/send?phone='+phone_no+'&text='+message)
        time.sleep(2)
        width,height = pg.size()
        pg.click(width/2,height/2)
        time.sleep(58)
        pg.press('enter')

def info(topic,lines=3):
    '''Gives information on the topic'''
    spe = wikipedia.summary(topic, sentences = lines)
    print(spe)
    
def playonyt(title):
    '''Opens YouTube video with following title'''
    url = 'https://www.youtube.com/results?q=' + title
    sc = requests.get(url)
    sctext = sc.text
    soup = BeautifulSoup(sctext,"html.parser")
    songs = soup.findAll("div",{"class":"yt-lockup-video"})
    song = songs[0].contents[0].contents[0].contents[0]
    songurl = song["href"]
    web.open("https://www.youtube.com"+songurl)

def search(topic):
    '''Searches about the topic on Google'''
    link = 'https://www.google.com/search?q={}'.format(topic)
    web.open(link)

try : 
    requests.get("https://www.google.com")
    current = time.time()
    tyme = current-last
        
except Exception:
    raise InternetException("NO INTERNET - Pywhatkit needs active internet connection")

if tyme >= 5:
        raise Warning("INTERNET IS SLOW, extraction of information might take longer time")

try :
    file = open("pywhatkit_history.txt","r")
    file.close()

except:
    file = open("pywhatkit_history.txt","w")
    print("Hello from the creator of pywhatkit, Ankit Raj Mahapatra.\nKindly do report bug if any.\nThis message will not be shown again.:)")
    file.write("--------------------")
    file.close()
    file = None
#end
