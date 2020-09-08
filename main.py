#! /usr/bin/python3

import os
import json
from time import sleep
from datetime import datetime
from colored import fg, attr
from fritzconnection.lib.fritzstatus import FritzStatus
import paho.mqtt.client as mqtt

def getFritzBoxReport(ip, password):
    print ("[~] Connecting to Fritz.Box ({ip})".format(ip=ip))
    fritzStatus = FritzStatus(address=fritzIP, password=fritzPassword)
    print ("[~] Requesting status information".format(ip=ip))
    statusReport = {
        "timestamp": str(datetime.now()),
        "external_ip": fritzStatus.external_ip,
        "external_ipv6": fritzStatus.external_ipv6,
        "bytes_received": fritzStatus.bytes_received, 
        "bytes_sent": fritzStatus.bytes_sent, 
        "is_connected": fritzStatus.is_connected,
        "is_linked": fritzStatus.is_linked,
        "bytes": fritzStatus.bytes_received,
        "max_byte_rate": {"up": fritzStatus.max_byte_rate[0], "down": fritzStatus.max_byte_rate[1]},
        "max_linked_bit_rate": {"up": fritzStatus.max_linked_bit_rate[0], "down": fritzStatus.max_linked_bit_rate[1]},
        "transmission_rate": {"up": fritzStatus.transmission_rate[0], "down": fritzStatus.transmission_rate[1]},
        "uptime": fritzStatus.uptime
    }
    if statusReport:
        print ("{color}[+] Successfully requested status information{reset}".format(color=fg(2), reset=attr(0)))
    return statusReport

def onMQTTConnect(client, userdata, flags, rc):
    if rc == 0:
        print ("{color}[+] Connected to MQTT broker (Return code: {rc}){reset}".format(color=fg(2), rc=rc, reset=attr(0)))
        client.publish("/fritzbox", "Hello World! Status reporter is running.")
    else:
        print ("{color}[-] Not connected to MQTT broker (Return code: {rc}){reset}".format(color=fg(1), rc=rc, reset=attr(0)))


def onMQTTPublish(client, userdata, mid):
    print ("{color}[*] Published to MQTT broker (Message ID: {mid}){reset}".format(color=fg(135), mid=mid, reset=attr(0)))

fritzPassword = os.environ["FRITZBOX_PASSWORD"]
fritzIP = os.environ["FRITZBOX_IP"]

mqttBroker = os.environ["MQTT_BROKER"]
mqttUsername = os.environ["MQTT_USERNAME"]
mqttPassword = os.environ["MQTT_PASSWORD"]
if "MQTT_PORT" in os.environ:
    mqttPort = os.environ["MQTT_PORT"]
else:
    mqttPort = 1883


client = mqtt.Client()
client.on_connect = onMQTTConnect
client.on_publish = onMQTTPublish
client.username_pw_set(username=mqttUsername, password=mqttPassword)
client.connect(mqttBroker, mqttPort, 60)
client.loop_start()

while True:
    report = getFritzBoxReport(fritzIP, fritzPassword)
    print (json.dumps(report, indent=1))
    client.publish("/fritzbox/report", json.dumps(report))
    sleep(60)
