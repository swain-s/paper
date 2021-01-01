from type import *

class Parse(object):
    def __init__(self):
        pass

    def parse_order(self, subject, message):
        event = Event()
        event.type = "order"
        event.status_list.append("cecv order")
        event.timestamp_list.append("current time")
        event.src_obj = subject


    def parse_message(self, message):
