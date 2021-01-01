from event_type import main_pool_event

e_p = []
a = main_pool_event()
a.event_id = 3
e_p.append(a)

def get_a_event(event_pool):
    if len(event_pool) == 0:
        current_event = main_pool_event()
    elif len(event_pool) > 0:
        current_event = event_pool[0]
    return current_event
