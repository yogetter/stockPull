#!/usr/bin/python
#coding=utf-8
import telnetlib, time, datetime
import requestSend

def refreshContent(connect):
    global content 
    content = connect.read_very_eager().decode('big5', 'ignore') 
    
def checkIndex(connect):
    refreshContent(connect)
    if u'請輸入代號' in content:
        return True
    else:
        return False

def checkLoginState():
    if u'歡迎您再度拜訪' in content:
        return 1 
    elif u'其它連線已登入此帳號' in content:
        return 2
    else:  
        return 0 ### Unknow State
    
def login(connect, user, passwd):
    connect.write(user + b'\r\n')
    connect.write(passwd + b'\r\n')
    time.sleep(5)
    connect.write(passwd + b'\r\n')
    refreshContent(connect)
    state = checkLoginState()
    if state == 1:
        connect.write(b'\r')
        time.sleep(1)
        connect.write(b'\r')
        return True
    elif state == 2:
        connect.write(b'N\r\n')
        return True
    elif state == 0:
        print "Unexpected error"
        return False
         
def stockPull(connect):
    connect.write(b's')
    connect.write(b'stock\r\n')
    connect.write(b'n')
    time.sleep(1)
    refreshContent(connect)     
    requestSend.checkPostId(content)

def checkTime():
    timeNow = datetime.datetime.now()
    hourMin = datetime.datetime.strftime(timeNow, '%H:%M')
    if int(hourMin.split(':')[0]) >= 13:
        return True 
    else:
        return False

host = 'ptt.cc'
user = 'user'
passwd = 'passwd'

while True:
    connect = telnetlib.Telnet(host)
    time.sleep(5)
    if checkIndex(connect):
        if login(connect, user, passwd):
            print "Connect success"
            break
    print "Connect failed, retry"

while True:
    if checkTime():
        print "Time is up, end program"
        break

    time.sleep(1)
    refreshContent(connect)
    stockPull(connect)
    time.sleep(60)

connect.close()
