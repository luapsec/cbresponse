#Script to query various states of a CBR Sensor

import argparse
import logging
import time

from datetime import datetime, timedelta
from cbapi.response.models import Sensor
from cbapi.response.rest_api import CbEnterpriseResponseAPI

logging.basicConfig(level=logging.INFO)

def main():
	
	parser = argparse.ArgumentParser(description='Check status of CBR sensor')
	parser.add_argument("-c", type=str, action="store", help="Computer to query.", required=True)
	args = parser.parse_args()
	
	#Connect to CB Response
	cb = CbEnterpriseResponseAPI()
	
	#Select hostname
	sensor = cb.select(Sensor).where("hostname:{0}".format(args.c))[0]
	
	print("\n Sensor Status      : ",sensor.status)
	print("Is sensor isolated? : "  ,sensor.is_isolating)
	print("Last Checkin        : "  ,sensor.last_checkin_time)
	print("Is sensor isolated  : "  ,sensor.uptime)
	print("Operating System    : "  ,sensor.os_environment_display_string)
	print("IP/MAC Address      : "  ,sensor.network_adapters)
	print("Group ID            : " ,sensor.group_id)

if __name__ == '__main__':
	main()
