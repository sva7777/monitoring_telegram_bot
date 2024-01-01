from threading import Event


class ThreadInfo:
    def __init__(self, event: Event, ip_address: str, chat_id: str, tool: str):
        self.event = event
        self.ip_address = ip_address
        self.chat_id = chat_id
        self.tool = tool

    def getDictionary(self, id: int):
        res = dict()
        res["id"] = id
        res["ip_address"] = self.ip_address
        res["chat_id"] = self.chat_id
        res["tool"] = self.tool

        return res
