import requests
from pprint import pprint
from http import HTTPStatus
from threading import Event


class TgSendMessage:
    def __init__(self, token: str, chat_id: int, ip_address: str, event: Event):
        self.token = token
        self.chat_id = chat_id
        self.ip_address = ip_address
        self.event = event

        message_down = f"Ping of device {self.ip_address} became failed"
        message_up = f"Ping of deice {self.ip_address} became successful"

        self.url_down = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}&text={message_down}"
        self.url_up = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}&text={message_up}"

    def get_message_up(self) -> str:
        return self.url_up

    def get_message_down(self) -> str:
        return self.url_down

    def send_message(self, message: str) -> bool:
        result = False

        try:
            res = requests.get(message)
            res.raise_for_status()
            result = True
        except requests.exceptions.HTTPError as errh:
            pprint("HTTP Error status code=" + str(errh.response.status_code))
            pprint("Reason=" + errh.response.reason)

            pprint("HTTP Error message=" + errh.response.text)

            if (
                errh.response.status_code == HTTPStatus.UNAUTHORIZED
                and errh.response.reason == "Unauthorized"
            ):
                # Token is not correct
                # ToDo: need to think how check Token ASAP
                pprint(
                    "Telegram token is not correct. Can not send message. Stop this monitoring"
                )
                self.event.set()

            if (
                errh.response.status_code == HTTPStatus.BAD_REQUEST
                and errh.response.reason == "Bad Request"
            ):
                # chat id is not correct
                # ToDo: need to think how check chat id ASAP
                pprint(
                    "Telegram chat id is not correct. Can not send message. Stop this monitoring"
                )
                self.event.set()

        except requests.exceptions.RequestException as errex:
            pprint("Exception request status code=" + str(errex.response.status_code))
            pprint("Exception request message=" + errex.response.text)

        return result
