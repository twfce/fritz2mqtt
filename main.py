#! /usr/bin/python3

import os
import json

from datetime import datetime
from fritzconnection.lib.fritzstatus import FritzStatus
from paho.mqtt.client as mqtt

fritzPassword = os.environ["FRITZBOX_PASSWORD"]
fritzIP = os.environ["FRITZBOX_IP"]
mqttBroker = os.environ["MQTT_IP"]
mqttUsername = os.environ["MQTT_USERNAME"]
mqttPassword = os.environ["MQTT_PASSWORD"]
mqttPort = os.environ["MQTT_PORT"]

fritzStatus = FritzStatus(address=fritzIP, password=fritzPassword)
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


