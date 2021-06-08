# The simple is just the beginning to open your mind of how everything works in a simple way. "GuiDeLuccaDev"

from pyzabbix import ZabbixMetric, ZabbixSender, ZabbixAPI
from flask import Flask, make_response, request
import os

app = Flask(__name__)

class ZABBIX():
    def __init__(self) -> None:
        self.zabbix_http = os.environ.get("ZABBIX_HTTP")
        self.zabbix_user = os.environ.get("ZABBIX_USER")
        self.zabbix_pass = os.environ.get("ZABBIX_PASS")
        self.zabbix_hostid = os.environ.get("ZABBIX_HOSTID")
        self.zabbix_server = os.environ.get("ZABBIX_SERVER")
        self.zabbix_port = int(os.environ.get("ZABBIX_PORT")) or 10051
        self.zabbix_host_name = ""
        self.zabbix_trap_key = ""

    def Getter(self):
        session = ZabbixAPI(self.zabbix_http, user=self.zabbix_user, password=self.zabbix_pass)

        all_hosts = session.host.get(monitored_hosts=1, output='extend')
        host = list(filter(lambda x:x["hostid"]==self.zabbix_hostid, all_hosts))
        self.zabbix_host_name = host[0]["host"]

        item = session.do_request("item.get", {"hostids": self.zabbix_hostid})
        
        if item["result"]:
            last_value = item["result"][0]["lastvalue"]
        else:
            last_value = None

        session.user.logout()
        return last_value

    def Sender(self, trap_key, trap_value):
        metric = [ZabbixMetric(self.zabbix_host_name, trap_key, trap_value)]
        
        zbx_connector = ZabbixSender(use_config=False, zabbix_server=self.zabbix_server, zabbix_port=self.zabbix_port)

        response = zbx_connector.send(metric).__dict__

        if response["_processed"] == 1 and response["_failed"] == 0:
            return {"host_name": self.zabbix_host_name, "trapper_key": trap_key, "changed_value": trap_value}
        else:
            return {"message": "Process Failed!"}

@app.route('/', methods=["POST", "GET"])
def index():
    try:
        received = request.data.decode("utf-8").replace("\\", "").split(":")
        
        ZBX = ZABBIX()
        last_value = ZBX.Getter()
        
        for parse in received:
            if "alerts" in parse:
                status = parse.replace('"', "").split(",")[0]
                
            if "commonLabels" in parse:
                trap_key = parse.replace('"', "").replace("}", "").split(",")[0]

        status_code = 200
        if status == "firing":
            if trap_key:
                if last_value == "0":
                    resp_sender = ZBX.Sender(trap_key, 1)
                else:
                    resp_sender = ZBX.Sender(trap_key, 0)

                resp_sender["status"] = status
            else:
               resp_sender = {"Error": "Trapper Key Not Found!", "Trapper": trap_key}
               status_code = 400
        else:
            resp_sender = ZBX.Sender(trap_key, last_value)
            resp_sender["status"] = status
            
        response = make_response(resp_sender, status_code)
        
        return response
            
    except Exception as err:
        return make_response({"error": err}, 400)

if __name__ == '__main__':
    app.run()