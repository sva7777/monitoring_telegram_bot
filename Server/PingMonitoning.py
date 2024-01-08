import threading
import subprocess
from threading import Event
import time
from datetime import datetime
from pprint import pprint
import requests
from collections import deque
from http import HTTPStatus


class PingMonThread(threading.Thread):
    def __init__(self, token: str, chat_id: int, ip_adress: str, event: Event):
        threading.Thread.__init__(self)

        self.token = token
        self.chat_id = chat_id
        self.ip_address = ip_adress
        self.event = event

        message_down = f"Ping of device {self.ip_address} became failed"
        message_up = f"Ping of deice {self.ip_address} became successful"

        self.url_down = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}&text={message_down}"
        self.url_up = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}&text={message_up}"

        # Queue to save the failed to send messages
        self.queue = deque()

    def sendMessage(self, message: str):
        result= False

        try:
            res = requests.get(message)
            res.raise_for_status()
            result = True
        except requests.exceptions.HTTPError as errh:
            pprint("HTTP Error status code=" + str(errh.response.status_code))
            pprint("Reason="+ errh.response.reason)

            pprint("HTTP Error message=" + errh.response.text)

            if errh.response.status_code == HTTPStatus.UNAUTHORIZED and errh.response.reason == "Unauthorized":
                # Token is not correct
                # ToDo: need to think how check Token ASAP
                pprint("Telegram token is not correct. Can not send message. Stop this monitoring")
                self.event.set()

            if errh.response.status_code == HTTPStatus.BAD_REQUEST and errh.response.reason == "Bad Request":
                # chat id is not correct
                   # ToDo: need to think how check chat id ASAP
                pprint("Telegram chat id is not correct. Can not send message. Stop this monitoring")
                self.event.set()


            # ToDo: add original time to message?
            self.queue.append(message)

        except requests.exceptions.RequestException as errex:
            pprint("Exception request status code=" + str(errex.response.status_code))
            pprint("Exception request message=" + errex.response.text)
            # ToDo: add original time to message?

            self.queue.append(message)

        return result

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
                self.sendMessage(self.url_down)

            if prestate == False and state == True:
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print("Current Time =", current_time)

                pprint("up")
                self.sendMessage(self.url_up)

            prestate = state

            while self.queue:
                message = self.queue.popleft()
                if self.sendMessage(message) == False:
                    # save messages order
                    self.queue.appendleft (message)
                    break

            time.sleep(2)
