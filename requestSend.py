#coding=utf-8
import requests
import json

def checkPostId(content):
    checkId = {u'MaInNine', u'chengwaye', u's10330076'}
    for Id in checkId:
        if Id in content:
            sendMessage()


def sendMessage():
    param = {
        'to':["$LineID1", "$LineID2"],
        'messages':[
            {
                'type':'text', 
                'text':u'$MESSAGE'
            }
        ]   
    }
    header = {
        'Authorization': '$TOKEN',
        'Content-Type': 'application/json'
    }
    r = requests.post('https://api.line.me/v2/bot/message/multicast', headers=header, data=json.dumps(param)) 
