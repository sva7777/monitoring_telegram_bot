import threading
import subprocess
from threading import Event
import time
from datetime import datetime
from pprint import pprint
import requests


# ToDo:

class PingMonThread(threading.Thread):
    def __init__(self, token:str , chat_id:int , ip_adress: str, event: Event):
        threading.Thread.__init__(self)

        self.token = token
        self.chat_id = chat_id
        self.ip_address = ip_adress
        self.event = event

    def ping(self):

        reply = subprocess.run(
            ["ping", "-c", "3", "-n", self.ip_address],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
        )
        if reply.returncode == 0:
            return True
        else:
            return False

    def run(self):
        # ToDo: may be move defines?
        message_down = f"устройство {self.ip_address} перестало пинговаться"
        message_up = f"устройство {self.ip_address} стало пинговаться"

        url_down = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}&text={message_down}"
        url_up = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}&text={message_up}"

        prestate = None

        while True:
            if self.event.is_set():
                break

            state = self.ping()

            if prestate == True and state == False:
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print("Current Time =", current_time)

                pprint("down")

                # pprint(requests.get(url_down))
            if prestate == False and state == True:
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print("Current Time =", current_time)

                pprint("up")
                # pprint(requests.get(url_up))

            prestate = state
            time.sleep(2)


