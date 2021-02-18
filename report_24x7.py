# The simple is just the beginning to open your mind of how everything works in a simple way. "GuiDeLuccaDev"

import requests
import csv

csvfile = open('d:/example.csv', 'w', newline='', encoding='utf-8')
c = csv.writer(csvfile)
c.writerow(["monitor_id", "display_name", "nic_name", "ip4_address"])

lista = []

url_monitors = "https://www.site24x7.com/app/api/monitors"
headers = {""}

monitor_response = requests.get(url_monitors, headers=headers)
monitors = monitor_response.json()
for monitor in monitors["data"]:
    nic_response = requests.get("https://www.site24x7.com/app/api/monitors/widget_details/"+monitor["monitor_id"]+"?period=2&widget_name=NetworkConfigDetails", headers=headers)
    nics = nic_response.json()
    if monitor["type"] == "SERVER" and monitor["state"] != "0":
        for nic in nics["data"]["widgets"]:
            c.writerow([monitor["monitor_id"],monitor["display_name"], nic["nic_name"], nic["ipv4_address"]])
            
    print(monitor["monitor_id"])

csvfile.close()
        

    



