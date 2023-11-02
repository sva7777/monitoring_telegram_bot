import subprocess
from pprint import pprint
import time
import sys
from datetime import datetime


# ToDo: add different monitoring tools
# ToDo: add monitoring tool parameters
def ping(ip_address):
    reply = subprocess.run(['ping', '-c', '3', '-n', ip_address],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           encoding='utf-8')
    if reply.returncode == 0:
        return True
    else:
        return False

# ToDo: neet to add support many devices prestate
prestate = None

import requests




if __name__=="__main__":

# ToDo: add support of many devices and chats
# ToDo: on fly add device(+chat) and remove it from monitoring. Need make server what performs job and clint to get and modify config

    if len(sys.argv) !=4:
        print("не корректные параметры скрипта. Правильные %Токен% %chat_id% %IP адрес%")
        sys.exit(1)
    TOKEN = sys.argv[1]
    chat_id = sys.argv[2]
    PING = sys.argv[3]
    print(PING)

    message_down = f"устройство {PING} перестало пинговаться"
    message_up = f"устройство {PING} стало пинговаться"

    url_down = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message_down}"
    url_up = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message_up}"


    while True:
        state = ping(PING)

        if prestate == True and state == False:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("Current Time =", current_time)

            pprint("down")

            #pprint(requests.get(url_down))
        if prestate == False and state == True:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("Current Time =", current_time)

            pprint("up")
            #pprint(requests.get(url_up))

        prestate= state
        time.sleep(2)

