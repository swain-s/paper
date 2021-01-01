import sm4
from test import date_pool_test

class event_sm4(object):
    def __init__(self):
        self.event_id = -1
        self.source_module = "test"


class date_sm4(object):
    def __init__(self):
        self.event_id = -1
        self.dest_module = ""
        #self.d_moudle = "sm3_module"
        self.date = b""

event_pool_sm4 = []
date_pool_sm4 = []

event0 = event_sm4()
event0.event_id = 0
event_pool_sm4.append(event0)


class sm3_moudule(object):
    #获取event_pool中的第一个event，返回current_event；根据current_event找到current_date
    def get_a_event(self, event_pool):
        current_event = event_sm4()
        current_date = date_sm4()
        if len(event_pool) > 0:
            current_event.event_id = event_pool[0].event_id
            current_date.event_id = current_event.event_id
            for date_test in date_pool_test:
                if date_test.event_id == current_event.event_id:
                    current_date.event_id = current_event.event_id
                    current_date.dest = "dest_moudle"
                    current_date.date = date_test.date
                    break
            del(event_pool[0])
            return current_event, current_date
        if len(event_pool_sm4) == 0:
            print("ok")
            return current_event, current_date

    def main(self):
        while True:
            (c_event, c_date) = self.get_a_event(event_pool_sm4)
            if c_event.event_id == -1:
                break
            elif c_event.event_id == 0:
                c_date.date = sm4.sm3_hash(c_date.date)
                print(c_date.date)

a = sm3_moudule()
a.main()