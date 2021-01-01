#功能模块：通信

# 为什么需要长度+记录：将原来的TCP报文分解为记录【类型】【长度】【数据】【MAC】，因为消息认证MAC，无需接收所有数据进行认证，按照记录进行认证
# 特性类型的记录，用于断开连接
# 1,hello| 类型 | 长度 | 【| SSL版本 | 随机数CR（32字节）| 会话ID | 支持的密码套件 | 支持的压缩方法 |】 ->

#       1,hello | 类型 | 长度 | 【 |SSL版本 | 随机数SR | 会话ID | 选择的密码套件 | 选择的压缩方法| 】  +
#       2, cert| 类型 | 长度 | 【 |证书版本 | 序列号 | 机构标识 | 公钥信息 | 证书有效期 | 密钥/证书用法（加密或签名）| 扩展 | 签名| 】 X.509证书（用于认证服务器） +
#       3,key| 类型 | 长度 | 【 |密钥交换 gb(gb = g^b (mod p))|】 （先生成随机数b）+
#       4,num| 类型 | 长度 | 【 |可接受的整数列表|】 +
#    <- 5,end| 类型 | 长度 |

# （验证）（计算预备密钥PM=gb^a (mod p) -[sha1、md5]->（计算主密钥48字节）-[sha1、md5]-> （计算密钥材料 128*6） 客MAC密钥 | 服MAC密钥 | 客加密密钥 | 服加密密钥 | 客初始向量 | 服初始向量
# | 类型 | 长度 | 【 |证书版本 | 序列号 | 机构标识 | 公钥信息 | 证书有效期 | 密钥/证书用法（加密或签名）| 扩展 | 签名| 】 X.509证书（用于认证客户端）
# | 类型 | 长度 | 【|ga(ga = g^a (mod p))|】| （先生成随机数a）
# | 类型 | 长度 |

#       （验证）（计算预备密钥PM=ga^b (mod p)）
# SSL记录协议
# SSL握手协议 TYPE = 22
# SSL更改密钥规格协议 TYPE = 20
# SSL警告协议 (握手或加解密出错) TYEP = 21

import random
import struct
import time
import sm_cypher_3
import sm2
import sm3
import sm4
import func

class SSLRecord(object):
    def __init__(self, ca_sm2_private, ca_sm2_public): #CA的私钥
        self.type = type
        self.lenth = 0
        self.message = b""
        self.mac = b""

        self.my_public = ca_sm2_public
        self.has_public = 1
        self.my_private = ca_sm2_private
        self.CA = sm2.CryptSM2(ca_sm2_public, ca_sm2_private)
        self.SM2 = sm2.CryptSM2(self.my_public, self.my_private)
        self.sm3 = None
        self.sm4 = None

    def random_num_256(self):
        current_num = b""
        cnt = 0
        while cnt < 256:
            cnt += 8
            num = random.randint(0, 255)
            current_num = current_num + struct.pack("!B", num)
        return current_num

    def random_hex_256(self):
        current_num = 0x0 & 0x0000000000000000000000000000000000000000000000000000000000000
        cnt = 0
        while cnt < 256:
            num = random.randint(0, 255)
            current_num = current_num ^ (num << cnt)
            cnt += 8
        return current_num

    def random_hex_16(self):
        current_num = 0x0 & 0x0000000000000000
        cnt = 0
        while cnt < 16:
            num = random.randint(0, 255)
            current_num = current_num ^ (num << cnt)
            cnt += 8
        return current_num

    def hex_to_byte(self, hex_256):
        current_byte = b""
        cnt = 256
        while cnt > 0:
            c_hex = hex_256
            cnt -= 8
            current_hex = ((c_hex << cnt) & 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF) >> 248
            current_byte = struct.pack("!B", current_hex) + current_byte
        return current_byte

    def byte_to_hex(self, byte_256):
        current_hex = 0x0 & 0x0000000000000000000000000000000000000000000000000000000000000
        cnt = 256
        my_tuple = struct.unpack("!32B", byte_256)
        pos = 0
        while cnt > 0:
            cnt -= 8
            current_hex = current_hex ^ (my_tuple[pos] << cnt)
            pos += 1
        return current_hex

    def random_num_32(self):
        current_num = b""
        cnt = 0
        while cnt < 32:
            cnt += 8
            num = random.randint(0, 256)
            current_num = current_num + struct.pack("!B", num)
        return current_num

    def hello(self):
        ssl_version = 1 #32 = 1
        random_int = self.random_num_256() #256 = 8
        session = 0 #32 = 1 客户端第一次连接服务器，该字段为空
        support_cypher = 17 # #16 = 0.5
        support_compress = 17 #16 = 0.5
        support = (support_cypher << 16) ^ support_compress

        hello_record = struct.pack("!I32sII", ssl_version, random_int, session, support)
        return hello_record

    def cert(self):
        cert_version = 1 #32 = 1
        cert_id = b"cert" #32 = 1
        depart_id = b"myca" #32 = 1
        if self.has_public == 0:
            self.my_public = self.random_num_256() #bytes 256bits
            self.has_public = 1
        my_public_key = self.my_public
        date = int(time.time()) #32 = 1
        useage = b"encr" #32 = 1
        #sign
        my_data = struct.pack("!I4s4s32sI4s", cert_version, cert_id, depart_id, my_public_key, date, useage) #160
        my_data_hash = sm3.sm3_hash(func.bytes_to_list(my_data)).encode('utf-8') #sm3后：256 bit (string)
        random_hex_str = func.random_hex(self.CA.para_len)
        sign = self.CA.sign(my_data_hash, random_hex_str) #data 应为bytes, sign为string, 128，即512bits
        #verify = self.sm2.verify(sign, my_data_hash)
        cert_record = struct.pack("52s128s", my_data, sign.encode('utf-8'))
        return cert_record

    def key_exchange(self):
        random_hex =self.random_hex_16() #16bit
        gab = ((2 ** random_hex) % 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF  #g为2或5， p为大素数
        gab_byte = self.hex_to_byte(gab)
        key_exchange_record = struct.pack("32s", gab_byte)
        print(key_exchange_record)
        print(len(key_exchange_record))
        #print(key_exchange_record)
        key_exchange_record = self.SM2.encrypt(key_exchange_record) #128 bytes，太长了
        print(key_exchange_record)
        print(len(key_exchange_record))

        print(len(self.SM2.encrypt(b"0123467890123456")))
        print(len(b"0123467890123456"))
        #print(self.SM2.decrypt(key_exchange_record))
        return key_exchange_record

    def request_cert(self):
        return


class SSL(object):
    def __init__(self):
        pass

    def ssl_send_hello(self):
        out_put = ""

private_key = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
S = SSLRecord(public_key, private_key)
S.key_exchange()

# 【类型】【长度】 【对称加密【【hash的前两个字节】【报文】】   【 对称加密（【时变参数=随机参数+1 + 标识session_id】【报文hash】）】




