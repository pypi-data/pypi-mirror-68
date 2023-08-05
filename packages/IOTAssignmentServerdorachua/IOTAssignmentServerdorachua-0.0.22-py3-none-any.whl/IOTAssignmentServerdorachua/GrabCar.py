from time import sleep
from IOTAssignmentUtilitiesdorachua.MySQLManager import MySQLManager
from IOTAssignmentUtilitiesdorachua.MySQLManager import QUERYTYPE_DELETE,QUERYTYPE_INSERT,QUERYTYPE_RETRIEVE,QUERYTYPE_UPDATE
from IOTAssignmentUtilitiesdorachua.OurCustomEncoder import OurCustomEncoder
import json
import sys

class GrabCar:
  
  def __init__(self, bid, u,pw,h,db):
    self.bookingid = bid
    self.user = u
    self.password = pw
    self.host = h
    self.database = db

  def getBookingID(self):
    return self.bookingid 

  def read(self, readtime):
    try:
      
      mysqlm = MySQLManager(self.user,self.password,self.host,self.database)
      result = mysqlm.connect()
      if result == True:
        sql = ("SELECT bookingid,accuracy,bearing,acceleration_x,acceleration_y,acceleration_z,gyro_x,gyro_y,gyro_z,seconds,speed,speedkmhour FROM telemetry WHERE bookingid=%(bookingid)s AND seconds=%(seconds)s")
        data = {'bookingid': self.bookingid , 'seconds': readtime}
        result = mysqlm.retrieve(QUERYTYPE_RETRIEVE, sql,data)
        if result == True:
          for (bookingid,accuracy,bearing,acceleration_x,acceleration_y,acceleration_z,gyro_x,gyro_y,gyro_z,seconds,speed,speedkmhour) in mysqlm.cursor:
            #print(f"At {seconds}, speed of {bookingid} was {speed}")
            output = {"bookingid": bookingid,"accuracy": accuracy, "bearing": bearing, 
                      "acceleration_x": acceleration_x,"acceleration_y": acceleration_y, "acceleration_z": acceleration_z, 
                      "gyro_x": gyro_x,"gyro_y": gyro_y, "gyro_z": gyro_z, 
                      "seconds":seconds,"speed":speed, "speedkmhour": speedkmhour}
            return json.dumps(output,cls=OurCustomEncoder)
        else:
            print(f"Error retrieving for {readtime}")
            #return json.dumps({"bookingid":-1},cls=ComplexEncoder)
            return None
      else:
          #return json.dumps({"bookingid":-1},cls=ComplexEncoder)
          return None

      mysqlm.disconnect()

    except TypeError as te:
      print("Encountering TypeError in GrabCar.read")
      for e in sys.exc_info():
        print(e)

    except ValueError as ve:
      print("Encountering ValueError in GrabCar.read")
      for e in sys.exc_info():
        print(e)

    except:
      print("Error ")
      print(sys.exc_info()[0])
      print(sys.exc_info()[1])
      #return json.dumps({"bookingid":-1},cls=ComplexEncoder)
      return None



