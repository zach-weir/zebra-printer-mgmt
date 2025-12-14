"""
    .SCRIPT NAME:   get_info.py
    .MODIFIED:      12.14.2025
    .USAGE:         py get_info.py [HOSTNAME_OR_IP] (ex: py get_info.py T1234PRT0201)

    .UPDATES:
    - 12.12.25 - initial creation
    - 12.13.25 - added query function
    - 12.14.25 - use separate data source for zebra commands
"""

import sys
import socket
from datetime import datetime
import time
import re
import json
import logging
from colorama import Fore, Back, Style 
from zebra_utilities import ZEBRA_MESSAGES, DATA_CATEGORIES

logging.basicConfig(
    filename = "server.log",
    level = logging.INFO,
    format = "%(asctime)s %(levelname)s %(message)s"
)

# function to connect to printer and obtain config data
def query_printer(search_param, zebra_commands):
    TCP_PORT = 9100
    BUFFER_SIZE = 512
    TCP_IP = search_param

    encoded_dict = {}
    received_dict = {}

    try:
        for key, value in zebra_commands.items():
            if isinstance(value, dict):
                encoded_dict[key] = value
            else:
                encoded_dict[key] = value.encode("utf-8")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            s.settimeout(10)
            s.connect((TCP_IP, TCP_PORT))

            for key, value in encoded_dict:
                MESSAGE = encoded_dict[key]
                s.send(MESSAGE)
                data = s.recv(BUFFER_SIZE)
                data_received = str(data, 'utf-8')
                received_dict[key] = data_received.strip().strip('"')
                time.sleep(0.1)  # sleep to prevent out of order results   

    except (TimeoutError, OSError, socket.timeout, socket.gaierror, socket.herror) as e:
        logging.error(f"{search_param} - unable to reach - {type(e).__name__}: {e}")
    finally:
        s.close()

    if "ZPL II" in received_dict["ZPL Mode"].upper():
        received_dict["ZPL Mode"] = "ZPL*"
    else:
        received_dict["ZPL Mode"] = "ZPL"

    received_dict["Ports"] = f"DEF: {received_dict['Default Port']} | ALT: {received_dict['Alternate Port']}"
    
    return received_dict

###############################
#        BEGIN  SCRIPT        #
###############################

time_start = datetime.now()  # start time

if len(sys.argv) != 2:
    print("INCORRECT USAGE -- Script must be run with site arguments - py get_printer_data.py <printer_hostname_or_ip>")
    sys.exit(1)

search_parameter = sys.argv[1]

try:
    if "10." in search_parameter:
        printer_id = search_parameter.strip()  # remove any spaces
    else:
        printer_id = socket.gethostbyname(search_parameter)
except (socket.gaierror) as e:
    logging.error(f"{search_parameter} - unknown host, not in DNS - {type(e).__name__}: {e}")
    sys.exit(1)

printer_data = query_printer(printer_id, ZEBRA_MESSAGES)

for key in printer_data:
    if key in ["Status", "MAC Address"]:
        printer_data[key] = str(printer_data.get(key, "")).upper()

for category, keys in DATA_CATEGORIES.items():
    print(Fore.CYAN + f"{category.upper()}" + Style.RESET_ALL +
          "\n--------------------------------------------------")
    for key in keys:
        if key in ["Default Port", "Alternate Port"]:
            pass
        value = printer_data.get(key, "")
        print(f"{key.ljust(25, '.')} {value}")
    print("\n", end='')

time_end = datetime.now()  # end time

###############################
#        FINISH SCRIPT        #
###############################

# calculate script duration
duration = time_end - time_start
total_seconds = int(duration.total_seconds())
hours = total_seconds // 3600
minutes = (total_seconds % 3600) // 60
seconds = total_seconds % 60
formatted_duration = f"{hours:02}:{minutes:02}:{seconds:02}"

logging.info(f"DURATION: {formatted_duration}")