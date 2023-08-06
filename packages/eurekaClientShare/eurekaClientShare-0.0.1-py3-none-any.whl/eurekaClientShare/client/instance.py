
import eurekaClientShare.constant.connection as CONN
from eurekaClientShare.constant.format import FORMAT
import json

class Instance:
    def __init__(self):
        self.__format = FORMAT
        self.__state = "STARTING"
        self.__set()

    def __set(self):
        self.__format["instance"]["hostName"] = CONN.HOSTINSTANCE
        self.__format["instance"]["app"] = CONN.SERVICENAME
        self.__format["instance"]["instanceId"] = "{}:{}:{}".format(CONN.HOSTINSTANCE, CONN.SERVICENAME, CONN.PORTINSTANCE)
        self.__format["instance"]["vipAddress"] = "{}{}:{}".format(CONN.PROTOCOL, CONN.HOSTINSTANCE, CONN.PORTINSTANCE)
        self.__format["instance"]["secureVipAddress"] = self.__format["instance"]["vipAddress"]
        self.__format["instance"]["ipAddr"] = self.__format["instance"]["vipAddress"]
        self.__format["instance"]["status"] = self.__state
        self.__format["instance"]["port"] = {"$": CONN.PORTINSTANCE, "@enabled": "true"}
        self.__format["instance"]["securePort"] = {"$": CONN.PORTINSTANCE, "@enabled": "true"}
        self.__format["instance"]["healthCheckUrl"] = "{}{}:{}/healthcheck".format(CONN.PROTOCOL, CONN.HOSTINSTANCE, CONN.PORTINSTANCE)
        self.__format["instance"]["statusPageUrl"] = "{}{}:{}/status".format(CONN.PROTOCOL, CONN.HOSTINSTANCE, CONN.PORTINSTANCE)
        self.__format["instance"]["homePageUrl"] = "{}{}:{}".format(CONN.PROTOCOL, CONN.HOSTINSTANCE, CONN.PORTINSTANCE)
        self.__format["instance"]["dataCenterInfo"] = {
			"@class": "com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo",
			"name": "MyOwn"
		}

    def setState(self, state):
        self.__state = state
        self.__set()
        return self

    def getStatus(self):
        return self.__state

    def getAppName(self):
        return self.__format["instance"]["app"]

    def getInstanceId(self):
        return self.__format["instance"]["instanceId"]

    def getDict(self):
        return self.__format

    def getString(self):
        return str(self.__format).replace("'", '"')

    def getJson(self):
        result = str(self.__format).replace("'", '"')
        return json.dumps(result)
