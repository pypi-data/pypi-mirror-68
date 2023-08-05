import asyncio
import sys
from random import randint,random
from datetime import datetime, timedelta 

import json
from IOTAssignmentUtilitiesdorachua import MySQLManager
from IOTAssignmentServerdorachua.GrabCarV2 import GrabCarV2
from IOTAssignmentServerdorachua.MyNewCarsFeederV2 import MyNewCarsFeederV2
import argparse

class MySocketServerV2:

    def __init__(self,u,pw,h,db):
        self.user = u
        self.password = pw
        self.host = h
        self.database = db
        self.isconnected = False
        self.feeder = None
        self.lastfeedtime = datetime.now()
        self.updateinterval = 2
        self.nextfeedtime = self.laststarttime + timedelta(minutes = self.updateinterval)

    def setNewCarsFeeder(self,feeder):
        self.feeder = feeder

    async def handle_client(self,reader, writer):

        try:            
            self.updateinterval = updateinterval            
            self.nextfeedtime = self.lastfeedtime + timedelta(minutes = self.updateinterval)
            timenow = datetime.now()
                        
            if timenow >= self.nextfeedtime and self.feeder is not None:
                self.lastfeedtime = self.nextfeedtime
                self.nextfeedtime = self.laststarttime + timedelta(minutes = self.updateinterval)
                newcars = self.feeder.createCars(5)
                
            data = await reader.read(100)
            message = data.decode("utf-8")
            requested_time = int(message)            
            addr = writer.get_extra_info('peername')

            dt = datetime.now()
            fn = f"{dt.year}-{dt.month}-{dt.day} {dt.hour}:{dt.minute}:{dt.second}"
            
            print(f"Received {message} from {addr} at {fn}")
            
            str_to_send = ""
            readings = []

            sfv2_list = self.feeder.getAllCars()
            
            for i in range(0,len(sfv2_list)):                
                
                reading = sfv2_list[i].read(requested_time-sfv2_list[i].offsetseconds)
                if reading is not None:
                    readings.append(reading)
                
            if len(readings)>0:
                
                writer.write(json.dumps(readings).encode("utf-8"))
                await writer.drain()            
            
                #print("Close the connection")

            writer.close()    
        
        except TypeError as te:
            print("Encountering TypeError in handle_client")
            for e in sys.exc_info():
                print(e)

        except ValueError as ve:
            print("Encountering ValueError in handle_client")
            for e in sys.exc_info():
                print(e)
        
        except KeyboardInterrupt:
            print('Interrupted')
            sys.exit()

        except:
            print("Error occurred in handle_client")
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])