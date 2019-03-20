import argparse
import logging
import time
from cbapi.response import *
logging.basicConfig(level=logging.INFO)

def main():

  #Command line options/help info
  parser = argparse.ArgumentParser(description='Isolate a Carbon Black Sensor')
  parser.add_argument("-c", type=str, action="store", help"Hostname to query.", required=True")
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
  
