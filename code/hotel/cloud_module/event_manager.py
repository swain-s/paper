from event_manager_h import *

if __name__ == "__main__":
    while True:
        current_event = get_a_event()
        if current_event.event_id == -1:
            continue
        elif current_event.event_id > 0:
            if current_event.source_module == "socket_in":
                continue
        else:
            print("something going to wrong")
            continue