#coding=utf-8
import telnetlib
import time
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
    
def login(connect, user, passwd):
    connect.write(user + b'\r\n')
    connect.write(passwd + b'\r\n')
    time.sleep(1)
    refreshContent(connect)     
    state = checkLoginState()
    if state == 1:
        connect.write(b'\r')
    elif state == 2:
        connect.write(b'N\r\n')
    time.sleep(1)
    refreshContent(connect)     
    stockPull(connect)

def stockPull(connect):
    connect.write(b's')
    connect.write(b'stock\r\n')
    connect.write(b'\r')
    time.sleep(1)
    refreshContent(connect)     
    requestSend.checkPostId(content)

host = 'ptt.cc'
user = 'user'
passwd = 'passwd'
connect = telnetlib.Telnet(host)
time.sleep(1)

if checkIndex(connect):
    login(connect, user, passwd)
    print "connect Success"
else:
    print content
    print "connect Failed"

connect.close()
