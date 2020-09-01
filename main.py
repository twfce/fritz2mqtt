#! /usr/bin/python3

import os
from fritzconnection.lib.fritzstatus import FritzStatus

fritzPassword = os.environ["FRITZBOX_PASSWORD"]
fritzIP = os.environ["FRITZBOX_IP"]

fritzStatus = FritzStatus(address=fritzIP, password=fritzPassword)
print(fritzStatus)
