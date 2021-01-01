#功能模块：国密算法模块
#本部分参考：https://github.com/gongxian-ding/gmssl-python

import math
import binascii
import copy

class SM3(object):
    def __init__(self):
        self.IV = [
            1937774191, 1226093241, 388252375, 3666478592,
            2842636476, 372324522, 3817729613, 2969243214,
        ]

        self.T_j = [
            2043430169, 2043430169, 2043430169, 2043430169, 2043430169, 2043430169,
            2043430169, 2043430169, 2043430169, 2043430169, 2043430169, 2043430169,
            2043430169, 2043430169, 2043430169, 2043430169, 2055708042, 2055708042,
            2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
            2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
            2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
            2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
            2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
            2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
            2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
            2055708042, 2055708042, 2055708042, 2055708042
        ]

    def rotl(self, x, n):
        return  ((x << n) & 0xffffffff) | ((x >> (32 - n)) & 0xffffffff)

    def sm3_ff_j(self, x, y, z, j):
        ret = None
        if 0 <= j and j < 16:
            ret = x ^ y ^ z
        elif 16 <= j and j < 64:
            ret = (x & y) | (x & z) | (y & z)
        return ret

    def sm3_gg_j(self, x, y, z, j):
        ret = None
        if 0 <= j and j < 16:
            ret = x ^ y ^ z
        elif 16 <= j and j < 64:
            # ret = (X | Y) & ((2 ** 32 - 1 - X) | Z)
            ret = (x & y) | ((~ x) & z)
        return ret

    def sm3_p_0(self, x):
        return x ^ (self.rotl(x, 9 % 32)) ^ (self.rotl(x, 17 % 32))

    def sm3_p_1(self, x):
        return x ^ (self.rotl(x, 15 % 32)) ^ (self.rotl(x, 23 % 32))

    def sm3_cf(self, v_i, b_i):
        w = []
        for i in range(16):
            weight = 0x1000000
            data = 0
            for k in range(i * 4, (i + 1) * 4):
                data = data + b_i[k] * weight
                weight = int(weight / 0x100)
            w.append(data)

        for j in range(16, 68):
            w.append(0)
            w[j] = self.sm3_p_1(w[j - 16] ^ w[j - 9] ^ (self.rotl(w[j - 3], 15 % 32))) ^ (self.rotl(w[j - 13], 7 % 32)) ^ w[j - 6]
            str1 = "%08x" % w[j]
        w_1 = []
        for j in range(0, 64):
            w_1.append(0)
            w_1[j] = w[j] ^ w[j + 4]
            str1 = "%08x" % w_1[j]

        a, b, c, d, e, f, g, h = v_i

        for j in range(0, 64):
            ss_1 = self.rotl(
                ((self.rotl(a, 12 % 32)) +
                 e +
                 (self.rotl(self.T_j[j], j % 32))) & 0xffffffff, 7 % 32
            )
            ss_2 = ss_1 ^ (self.rotl(a, 12 % 32))
            tt_1 = (self.sm3_ff_j(a, b, c, j) + d + ss_2 + w_1[j]) & 0xffffffff
            tt_2 = (self.sm3_gg_j(e, f, g, j) + h + ss_1 + w[j]) & 0xffffffff
            d = c
            c = self.rotl(b, 9 % 32)
            b = a
            a = tt_1
            h = g
            g = self.rotl(f, 19 % 32)
            f = e
            e = self.sm3_p_0(tt_2)

            a, b, c, d, e, f, g, h = map(
                lambda x: x & 0xFFFFFFFF, [a, b, c, d, e, f, g, h])

        v_j = [a, b, c, d, e, f, g, h]
        return [v_j[i] ^ v_i[i] for i in range(8)]

    def sm3_hash(self, msg):
        # print(msg)
        len1 = len(msg)
        reserve1 = len1 % 64
        msg.append(0x80)
        reserve1 = reserve1 + 1
        # 56-64, add 64 byte
        range_end = 56
        if reserve1 > range_end:
            range_end = range_end + 64

        for i in range(reserve1, range_end):
            msg.append(0x00)

        bit_length = (len1) * 8
        bit_length_str = [bit_length % 0x100]
        for i in range(7):
            bit_length = int(bit_length / 0x100)
            bit_length_str.append(bit_length % 0x100)
        for i in range(8):
            msg.append(bit_length_str[7 - i])

        group_count = round(len(msg) / 64)

        B = []
        for i in range(0, group_count):
            B.append(msg[i * 64:(i + 1) * 64])

        V = []
        V.append(self.IV)
        for i in range(0, group_count):
            V.append(self.sm3_cf(V[i], B[i]))

        y = V[i + 1]
        result = ""
        for i in y:
            result = '%s%08x' % (result, i)
        return result

    def sm3_kdf(self, z, klen):  # z为16进制表示的比特串（str），klen为密钥长度（单位byte）
        klen = int(klen)
        ct = 0x00000001
        rcnt = math.ceil(klen / 32)
        zin = [i for i in bytes.fromhex(z.decode('utf8'))]
        ha = ""
        for i in range(rcnt):
            msg = zin + [i for i in binascii.a2b_hex(('%08x' % ct).encode('utf8'))]
            ha = ha + self.sm3_hash(msg)
            ct += 1
        return ha[0: klen * 2]

#&：按位与；|：按位或；^按位异或
#0x=\x 16进制数 =1字节  \u = 1字（unicode）
xor = lambda a, b:list(map(lambda x, y: x ^ y, a, b)) #按位异或并返回数组；输入：两个字符串即byte串b""-->每个字母按ascll编码(a-->97, 1-->49)-->list【对应字母位异或]-->list[]元素^list[]元素
#lambda匿名函数：可无标识符、任意参数、无命令、一个表达式；map(lambda:,)遍历、filter()筛选、reduce()相加
rotl = lambda x, n:((x << n) & 0xffffffff) | ((x >> (32 - n)) & 0xffffffff)#字x循环（32）左移n位；输入：16进制数x,10进制数n（你<32）-->16进制数到二进制-->循环左移x_2左移n位
get_uint32_be = lambda key_data:((key_data[0] << 24) | (key_data[1] << 16) | (key_data[2] << 8) | (key_data[3]))
put_uint32_be = lambda n:[((n>>24)&0xff), ((n>>16)&0xff), ((n>>8)&0xff), ((n)&0xff)]
padding = lambda data, block=16: data + [(16 - len(data) % block)for _ in range(16 - len(data) % block)]
unpadding = lambda data: data[:-data[-1]]
list_to_bytes = lambda data: b''.join([bytes((i,)) for i in data])
bytes_to_list = lambda data: [i for i in data]

#Expanded SM4 box table
SM4_BOXES_TABLE = [
    0xd6,0x90,0xe9,0xfe,0xcc,0xe1,0x3d,0xb7,0x16,0xb6,0x14,0xc2,0x28,0xfb,0x2c,
    0x05,0x2b,0x67,0x9a,0x76,0x2a,0xbe,0x04,0xc3,0xaa,0x44,0x13,0x26,0x49,0x86,
    0x06,0x99,0x9c,0x42,0x50,0xf4,0x91,0xef,0x98,0x7a,0x33,0x54,0x0b,0x43,0xed,
    0xcf,0xac,0x62,0xe4,0xb3,0x1c,0xa9,0xc9,0x08,0xe8,0x95,0x80,0xdf,0x94,0xfa,
    0x75,0x8f,0x3f,0xa6,0x47,0x07,0xa7,0xfc,0xf3,0x73,0x17,0xba,0x83,0x59,0x3c,
    0x19,0xe6,0x85,0x4f,0xa8,0x68,0x6b,0x81,0xb2,0x71,0x64,0xda,0x8b,0xf8,0xeb,
    0x0f,0x4b,0x70,0x56,0x9d,0x35,0x1e,0x24,0x0e,0x5e,0x63,0x58,0xd1,0xa2,0x25,
    0x22,0x7c,0x3b,0x01,0x21,0x78,0x87,0xd4,0x00,0x46,0x57,0x9f,0xd3,0x27,0x52,
    0x4c,0x36,0x02,0xe7,0xa0,0xc4,0xc8,0x9e,0xea,0xbf,0x8a,0xd2,0x40,0xc7,0x38,
    0xb5,0xa3,0xf7,0xf2,0xce,0xf9,0x61,0x15,0xa1,0xe0,0xae,0x5d,0xa4,0x9b,0x34,
    0x1a,0x55,0xad,0x93,0x32,0x30,0xf5,0x8c,0xb1,0xe3,0x1d,0xf6,0xe2,0x2e,0x82,
    0x66,0xca,0x60,0xc0,0x29,0x23,0xab,0x0d,0x53,0x4e,0x6f,0xd5,0xdb,0x37,0x45,
    0xde,0xfd,0x8e,0x2f,0x03,0xff,0x6a,0x72,0x6d,0x6c,0x5b,0x51,0x8d,0x1b,0xaf,
    0x92,0xbb,0xdd,0xbc,0x7f,0x11,0xd9,0x5c,0x41,0x1f,0x10,0x5a,0xd8,0x0a,0xc1,
    0x31,0x88,0xa5,0xcd,0x7b,0xbd,0x2d,0x74,0xd0,0x12,0xb8,0xe5,0xb4,0xb0,0x89,
    0x69,0x97,0x4a,0x0c,0x96,0x77,0x7e,0x65,0xb9,0xf1,0x09,0xc5,0x6e,0xc6,0x84,
    0x18,0xf0,0x7d,0xec,0x3a,0xdc,0x4d,0x20,0x79,0xee,0x5f,0x3e,0xd7,0xcb,0x39,
    0x48,
]

# System parameter
SM4_FK = [0xa3b1bac6,0x56aa3350,0x677d9197,0xb27022dc]

# fixed parameter
SM4_CK = [
    0x00070e15,0x1c232a31,0x383f464d,0x545b6269,
    0x70777e85,0x8c939aa1,0xa8afb6bd,0xc4cbd2d9,
    0xe0e7eef5,0xfc030a11,0x181f262d,0x343b4249,
    0x50575e65,0x6c737a81,0x888f969d,0xa4abb2b9,
    0xc0c7ced5,0xdce3eaf1,0xf8ff060d,0x141b2229,
    0x30373e45,0x4c535a61,0x686f767d,0x848b9299,
    0xa0a7aeb5,0xbcc3cad1,0xd8dfe6ed,0xf4fb0209,
    0x10171e25,0x2c333a41,0x484f565d,0x646b7279
]

SM4_ENCRYPT = 0
SM4_DECRYPT = 1

class CryptSM4(object):

    def __init__(self, mode=SM4_ENCRYPT):
        self.sk = [0]*32
        self.mode = mode

    # Calculating round encryption key.
    # args:    [in] a: a is a 32 bits unsigned value;
    # return: sk[i]: i{0,1,2,3,...31}.
    @classmethod
    def _round_key(cls, ka):
        b = [0, 0, 0, 0]
        a = put_uint32_be(ka)
        b[0] = SM4_BOXES_TABLE[a[0]]
        b[1] = SM4_BOXES_TABLE[a[1]]
        b[2] = SM4_BOXES_TABLE[a[2]]
        b[3] = SM4_BOXES_TABLE[a[3]]
        bb = get_uint32_be(b[0:4])
        rk = bb ^ (rotl(bb, 13)) ^ (rotl(bb, 23))
        return rk

    # Calculating and getting encryption/decryption contents.
    # args:    [in] x0: original contents;
    # args:    [in] x1: original contents;
    # args:    [in] x2: original contents;
    # args:    [in] x3: original contents;
    # args:    [in] rk: encryption/decryption key;
    # return the contents of encryption/decryption contents.
    @classmethod
    def _f(cls, x0, x1, x2, x3, rk):
        # "T algorithm" == "L algorithm" + "t algorithm".
        # args:    [in] a: a is a 32 bits unsigned value;
        # return: c: c is calculated with line algorithm "L" and nonline algorithm "t"
        def _sm4_l_t(ka):
            b = [0, 0, 0, 0]
            a = put_uint32_be(ka)
            b[0] = SM4_BOXES_TABLE[a[0]]
            b[1] = SM4_BOXES_TABLE[a[1]]
            b[2] = SM4_BOXES_TABLE[a[2]]
            b[3] = SM4_BOXES_TABLE[a[3]]
            bb = get_uint32_be(b[0:4])
            c = bb ^ (rotl(bb, 2)) ^ (rotl(bb, 10)) ^ (rotl(bb, 18)) ^ (rotl(bb, 24))
            return c
        return (x0 ^ _sm4_l_t(x1 ^ x2 ^ x3 ^ rk))

    def set_key(self, key, mode):
        key = bytes_to_list(key)
        MK = [0, 0, 0, 0]
        k = [0]*36
        MK[0] = get_uint32_be(key[0:4])
        MK[1] = get_uint32_be(key[4:8])
        MK[2] = get_uint32_be(key[8:12])
        MK[3] = get_uint32_be(key[12:16])
        k[0:4] = xor(MK[0:4], SM4_FK[0:4])
        for i in range(32):
            k[i + 4] = k[i] ^ (
                self._round_key(k[i + 1] ^ k[i + 2] ^ k[i + 3] ^ SM4_CK[i]))
            self.sk[i] = k[i + 4]
        self.mode = mode
        if mode == SM4_DECRYPT:
            for idx in range(16):
                t = self.sk[idx]
                self.sk[idx] = self.sk[31 - idx]
                self.sk[31 - idx] = t

    def one_round(self, sk, in_put):
        out_put = []
        ulbuf = [0]*36
        ulbuf[0] = get_uint32_be(in_put[0:4])
        ulbuf[1] = get_uint32_be(in_put[4:8])
        ulbuf[2] = get_uint32_be(in_put[8:12])
        ulbuf[3] = get_uint32_be(in_put[12:16])
        for idx in range(32):
            ulbuf[idx + 4] = self._f(ulbuf[idx], ulbuf[idx + 1], ulbuf[idx + 2], ulbuf[idx + 3], sk[idx])

        out_put += put_uint32_be(ulbuf[35])
        out_put += put_uint32_be(ulbuf[34])
        out_put += put_uint32_be(ulbuf[33])
        out_put += put_uint32_be(ulbuf[32])
        return out_put

    def crypt_ecb(self, input_data):
        # SM4-ECB block encryption/decryption
        input_data = bytes_to_list(input_data)
        if self.mode == SM4_ENCRYPT:
            input_data = padding(input_data)
        length = len(input_data)
        i = 0
        output_data = []
        while length > 0:
            output_data += self.one_round(self.sk, input_data[i:i+16])
            i += 16
            length -= 16
        if self.mode == SM4_DECRYPT:
            return list_to_bytes(unpadding(output_data))
        return list_to_bytes(output_data)

    def crypt_cbc(self, iv, input_data):
        #SM4-CBC buffer encryption/decryption
        i = 0
        output_data = []
        tmp_input = [0]*16
        iv = bytes_to_list(iv)
        if self.mode == SM4_ENCRYPT:
            input_data = padding(bytes_to_list(input_data))
            length = len(input_data)
            while length > 0:
                tmp_input[0:16] = xor(input_data[i:i+16], iv[0:16])
                output_data += self.one_round(self.sk, tmp_input[0:16])
                iv = copy.deepcopy(output_data[i:i+16])
                i += 16
                length -= 16
            return list_to_bytes(output_data)
        else:
            length = len(input_data)
            while length > 0:
                output_data += self.one_round(self.sk, input_data[i:i+16])
                output_data[i:i+16] = xor(output_data[i:i+16], iv[0:16])
                iv = copy.deepcopy(input_data[i:i + 16])
                i += 16
                length -= 16
            return list_to_bytes(unpadding(output_data))
