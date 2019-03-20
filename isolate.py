#Script will:
# Isolate the endpoint
# Send message to user informing them their computer has been isolated, you may want to remove this if you believe it's an insider threat etc
# Sync all events from sensor with server so they available in CBR asap
# Check with server that endpoint has been isolated, found this takes around 30 seconds to isolate an endpoint but longer for it to report back properly

import argparse
import logging
import time
from cbapi.response import *
logging.basicConfig(level=logging.INFO)

def main():

  #Command line options/help info
  parser = argparse.ArgumentParser(description='Isolate a Carbon Black Sensor')
  parser.add_argument("-c", type=str, action="store", help="Computer to isolate.", required=True)
  args = parser.parse_args()
  
  #Connect to CB Response
  cb = CBEnterpriseResponseAPI()
  #Select sensor from command line
  sensor = cb.select(Sensor).where("hostname:{0}".format(args.c))[0]
  
  #Isolate sensor
  sensor.network_isolation_enabled = True
  sensor.save
  
  #Print status of sensor, making sure it's online
  print("Sensor status:",sensor.status)
  print("Sending message to user and checking if sensor is now isolated")
  
  #Display Message to user via Live Response (Windows only, via msg console..)
  with sensor.lr_session() as session:
    print(session.create_process(r'cmd.exe /c "msg /TIME:619200 console PC Isolated - Contact extension 0 "'))
  
  print("\n Message sent to user\n")  
    
  #Sync all events from sensor with server  
  sensor.flush_events()
  print("Command sent to isolate.. checking status of sensor")
  
  isolated = False
  while isolated == False:
    check = cb.select(Sensor).where("hostname:{0}".format(args.c))[0]
    isolated = check.is_isolating
    print("Isolation enabled?", check.is_isolating)
    time.sleep(30)
    
if __name__ == '__main__':
  main()
  
