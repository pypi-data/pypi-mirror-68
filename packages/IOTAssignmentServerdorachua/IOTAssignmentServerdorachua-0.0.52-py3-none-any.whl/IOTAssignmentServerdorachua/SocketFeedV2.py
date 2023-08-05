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

        #id,bookingid,bookingidwithtime,offsetseconds,startdatetime_value,enddatetime_value,timestamp_Value
        self.id = record[0]
        self.bookingid = record[1]
        self.bookingidwithtime = record[2]
        self.offsetseconds = record[3]
        self.startdatetime_value = record[4]
        self.enddatetime_value = record[5]
        self.timestamp_value = record[6]
    