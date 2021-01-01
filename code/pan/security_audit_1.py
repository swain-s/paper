#功能模块：安全审计

import time_related

class AuditMessage(object):
    def __init__(self, type):
        self.type = type
        self.time = ""
        self.describe = ""
        self.message = ""

class AuditMessageQueue(object):
    def __init__(self):
        self.audit_process = None
        self.audit_message_queue = []
        self.signal = 0
        self.audit_process_queue = []

    def audit_queue_push(self, audit_message):
        pass

    def audit_queue_pop(self):
        pass

#审计一： 网络接口socket审计
#   相关API：接受连接、接收数据、发送数据
class SocektAudit(object):
    def __init__(self):
        pass

    def s_send_audit(self, process, recv_ip, recv_port, message, audit_message_queue):
        AuditDate = AuditMessage("socket_send")
        Time = time_related.Time()
        AuditDate.time = Time.current_time()
        AuditDate.describe = "From %s:%s to %s:%s" % (process.ip, process.port, recv_ip, recv_port)
        AuditDate.message = message

        audit_message_queue.add_queue_push(AuditDate)

    def s_recv_audit(self, process, send_ip, send_port, message, audit_message_queue):
        AuditDate = AuditMessage("socket_recv")
        Time = time_related.Time()
        AuditDate.time = Time.current_time()
        AuditDate.describe = "From %s:%s to %s:%s" % (send_ip, send_port, process.ip, process.port)
        AuditDate.message = message

        audit_message_queue.add_queue_push(AuditDate)
