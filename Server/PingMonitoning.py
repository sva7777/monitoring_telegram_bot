import threading
import subprocess
from threading import Event
import time
from datetime import datetime
from pprint import pprint
from collections import deque
from Telegram.TgSendMessage import TgSendMessage


class PingMonThread(threading.Thread):
    def __init__(self, ip_address: str, event: Event, sender: TgSendMessage):
        threading.Thread.__init__(self)
        self.event = event
        self.ip_address = ip_address
        self.sender = sender

        # Queue to save the failed to send messages
        self.queue = deque()

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

                # ToDo: I don't like how I get message to resend
                message = self.sender.get_message_down()
                if self.sender.send_message(message) == False:
                    self.queue.append(message)

            if prestate == False and state == True:
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print("Current Time =", current_time)

                pprint("up")

                # ToDo: I don't like how I get message to resend
                message = self.sender.get_message_up()
                if self.sender.send_message(message) == False:
                    self.queue.append(message)

            prestate = state

            while self.queue:
                message = self.queue.popleft()
                if self.sender.send_message(message) == False:
                    # save messages order
                    self.queue.appendleft(message)
                    break

            time.sleep(2)
