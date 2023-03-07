from notifiers import get_notifier
from info import token,id

def bet_siska(data):
    telegram = get_notifier('telegram')
    info = "\n".join([i for i in data])
    telegram.notify(token=token,chat_id = id,message = info)
    print("MSG HAS BEEN SENT")

def errormsg():
    telegram = get_notifier('telegram')
    message = "RESTART HANDBALL SCRIPT!!!"
    telegram.notify(token=token,chat_id = id,message = message)


def made_mistake():
    telegram = get_notifier('telegram')
    message = "HANDBALL MISTAKE!!!"
    telegram.notify(token=token,chat_id = id,message = message)
    print("HANDBALL MISTAKE!")


