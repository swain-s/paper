import time
import threading

#struct
class timer_event(object):
    def __init__(self):
        self.timer_event_id = 0
        self.timer_type = ""
        self.begin_time = 0
        self.last_time = 0
        self.before_timer_event = None
        self.next_timer_event = None

#struct
class head_tiemr_event(object):
    def __init__(self):
        self.timer_type = ""
        self.timer_event_count = 0
        self.avai_id = 0
        self.first_timer_event_mode = 0
        self.first_timer_event = None

class Timer(object):
    def __init__(self):
        self.current_time = 0
        self.list_timer_event = []

    def main_timer_thread_funnc(self):
        for i in range(20):
            time.sleep(1)
            print("+")
            self.current_time += 1

    def main_timer_thread_start(self):
        self.timer_thread = threading.Thread(target=self.main_timer_thread_funnc)
        self.timer_thread.start()

    def init_list_timer(self):
        self.timer_head = head_tiemr_event()
        self.timer_head.timer_event_count = 0
        self.timer_head.first_timer_event_mode = None

    def add_a_timer_event(self):
        a_timer_event = timer_event()
        a_timer_event.timer_event_id = self.timer_head.avai_id
        a_timer_event.begin_time = self.current_time
        a_timer_event.next_timer_event = None
        a_timer_event.before__timer_event = None

        last_event = self.timer_head.first_timer_event
        for i in range(self.timer_head.timer_event_count):
            if last_event == None:
                print("add timer event error")
                return -1
            last_event = last_event.next_timer_event

        last_event.next_timer_event = a_timer_event
        a_timer_event.last_timer_event = last_event
        self.timer_head.timer_event_count += 1
        self.timer_head.avai_id += 1

        return a_timer_event.timer_event_id

    def destroy_timer(self, id):
        current_event = self.timer_head.first_timer_event
        for i in range(self.timer_head.timer_event_count):
            if current_event.timer_event_id == id:
                break
            elif i == range(self.timer_head.timer_event_count-1) and current_event.timer_event_id != id:
                print("error: can't find: %d" % id)
                return -1
            current_event = current_event.next_timer_event

        current_event.before_timer_event.next_timer_event = current_event.next_timer_event
        del current_event

        return 0

    def get_runtime(self, ):
        current_event = self.timer_head.first_timer_event
        for i in range(self.timer_head.timer_event_count):
            if current_event.timer_event_id == id:
                break
            elif i == range(self.timer_head.timer_event_count - 1) and current_event.timer_event_id != id:
                print("error: can't find: %d" % id)
                return -1
            current_event = current_event.next_timer_event
        return (self.current_time - current_event.begin_time)