from type import *

class EventParser(object):
    def __init__(self):
        pass

    def parse_net_event(self):
        pass


class OrderParser(object):
    def __init__(self, recv_con_pool, send_con_pool):
        self.me = None
        self.cur_client_name = ""
        self.recv_pool = recv_con_pool
        self.send_pool = send_con_pool

    def parse_raw_order(self, raw_order):
        if (len(raw_order) < 2):
            return None

        order_type_flag = raw_order[0]
        real_order = raw_order[1:].strip()

        if order_type_flag == '@':
            pass
            #self.parse_switch_order(real_order)
        elif order_type_flag == 'S':
            self.parse_sql_order(real_order)
        elif order_type_flag == 'E':
            pass
        elif order_type_flag == 'C':
            pass
        elif order_type_flag == 'A':
            pass
        elif order_type_flag == 'M':
            pass
        else:
            pass


    def parse_switch_order(self, event, switch_order):
        # input : event
        #   type = read commond
        #   status = [read]
        #   src_obj = me
        # output : event +
        #   dest_obj =
        #   order_plus =

        event.status.refresh("start parse")

        order_plus = OrderPlus("@", switch_order)
        if switch_order == self.me:
            event.status.refresh("finish")
            return event
        else:
            for recv_subj in self.recv_pool:
                if recv_subj.name == switch_order:
                    event.dest_obj = recv_subj
                    if recv_subj.sock == None:
                        pass
                    event.status.refresh("end parse")
                    return event
            for send_subj in self.send_pool:
                if send_subj.name == switch_order:
                    event.dest_obj = send_subj
                    event.status.refresh("end parse")
                    return event



        event.order_plus.next = "finish"
        event.dest_obj = None


    def parse_sql_order(self, sql_order):
        pass

    def parse_extra_order(self, extra_order):
        pass

    def parse_config_order(self, config_order):
        pass

    def parse_alice_order(self, alice_order):
        pass

    def parse_math_order(self, math_order):
        pass

    def parse_shell_order(self, shell_order):
        pass

    def parse_recv_order(self, recv_order):
        pass