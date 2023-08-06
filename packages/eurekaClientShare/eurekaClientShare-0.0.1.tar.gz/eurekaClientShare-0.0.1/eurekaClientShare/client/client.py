
from eurekaClientShare.client.instance import Instance
from eurekaClientShare.util.request import Request
import eurekaClientShare.constant.connection as CONN
import eurekaClientShare.constant.http_code as CODE
import time
from threading import Thread

class DiscoveryClient:
    def __init__(self):
        self.__instance = Instance()
        self.__beat = int(CONN.HEARTBEATDISCOVER)
        self.__beats = 0
        self.__url = "{}/{}".format(CONN.HOSTDISCOVER, self.__instance.getAppName())
        self.headers = {"Content-Type": "application/json"}
        self.__create()
        self.__instance.setState("UP")
        self.startHeartbeat()


    def __create(self):
        urlDelete = "{}/{}".format(self.__url, self.__instance.getInstanceId())
        Request(url=urlDelete, headers=self.headers).DELETE()
        result = Request(url=self.__url, body=self.__instance.getDict(), headers=self.headers).POST()
        return result

    def __heartbeat(self):
        while self.__instance.getStatus() == "UP":
            time.sleep(self.__beat)
            self.__send()
        return

    def __send(self):
        self.__beats += 1
        urlInstance = "{}/{}/status?value={}".format(self.__url, self.__instance.getInstanceId(), self.__instance.getStatus())
        result = Request(url=urlInstance, headers=self.headers).PUT()
        return result

    def startHeartbeat(self):
        self.__heart = Thread(target=self.__heartbeat)
        self.__heart.daemon = True
        self.__heart.start()
        return

    def stop(self):
        self.__instance.setState("DOWN")
        self.__send()
        return 1
