event_id = [i for i in range(0, 1000)]
used_id = []

type_connection = ["socket_in_module"]  #socket connection
type_hand = ["socket_in_module", "token_datebase_module", "random_module", "sm9_ike_module", "sm3_module", "key_datebase_module", "socket_out_module"]    #SM9握手阶段

type_hello = ["socket_in_module", "key_datebase_module", "token_datebase_module", "sm3_module", "sm4_module", "socket_out_module"]     #hello
type_user_r = []    #_r:顾客注册
type_password_r = []
type_face_r = []
type_id_r = []
type_cookie= []
type_book = []
type_hotel_id = []
type_face_a = []    #_a：酒店身份认证
type_qrcode_a = []

#主事件池的事件
class main_pool_event(object):
    def __init__(self):
        self.event_id = -1

        self.event_type = -1
        self.last_module = ""
        self.last_module_event_id = -1

#字符/块设备：socket接收模块的事件
class socket_in_pool_event(object):
    def __init__(self):
        self.socket_in_event_id = -1

        self.