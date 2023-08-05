from time import sleep
from IOTAssignmentUtilitiesdorachua.MySQLManager import MySQLManager
from IOTAssignmentUtilitiesdorachua.MySQLManager import QUERYTYPE_DELETE,QUERYTYPE_INSERT,QUERYTYPE_RETRIEVE,QUERYTYPE_UPDATE
from IOTAssignmentUtilitiesdorachua.OurCustomEncoder import OurCustomEncoder
import json
import sys
from datetime import datetime,timedelta
#from IOTAssignmentUtilitiesdorachua.MyDateTimeUtilities import MyDateTimeUtilities

class SocketFeedV2:
  
    def __init__(self,record, u,pw,h,db):        
        self.user = u
        self.password = pw
        self.host = h
        self.database = db

        print(record)

        #self.id = record["id"]
        #self.bookingid = record["bookingid"]
        #self.bookingidwithtime = record['bookingidwithtime']
        #self.offsetseconds = record['offsetsecords']
        #self.startdatetime_value = record['startdatetime_value']
        #self.enddatetime_value = record['enddatetime_value']
        #self.timestamp_value = record['timestamp_value']

        

        
    