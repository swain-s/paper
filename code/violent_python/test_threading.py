import time
import threading

def run(num):  #子线程运行函数
    print('函数开始',num)
    time.sleep(3)
    print('函数结束',num)
def main():  #主线程运行函数
    for i in range(4): #在主线程中运行4个子线程
        t1 = threading.Thread(target=run,args=(i,))
        print('启动线程',t1.getName())
        t1.start()
#        time.sleep(3)
#        t1.join()
 #       print('结束线程',t1.getName())


m = threading.Thread(target=main,args=())
#m.setDaemon(True) #设置主线程为守护线程
print('开启主线程')
m.start()
m.join(timeout=1) #等待3秒后主线程退出，不管子线程是否运行完

print('结束主线程')