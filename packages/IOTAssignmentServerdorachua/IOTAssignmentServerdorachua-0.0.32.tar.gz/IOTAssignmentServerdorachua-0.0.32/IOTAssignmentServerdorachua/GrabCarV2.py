from time import sleep,timedelta
from IOTAssignmentUtilitiesdorachua.MySQLManager import MySQLManager
from IOTAssignmentUtilitiesdorachua.MySQLManager import QUERYTYPE_DELETE,QUERYTYPE_INSERT,QUERYTYPE_RETRIEVE,QUERYTYPE_UPDATE
from IOTAssignmentUtilitiesdorachua.OurCustomEncoder import OurCustomEncoder
import json
import sys
from datetime import datetime
from IOTAssignmentUtilitiesdorachua import MyDateTimeUtilities

class GrabCarV2:
  
    def __init__(self,appstarttime,bid, u,pw,h,db):        
        self.user = u
        self.password = pw
        self.host = h
        self.database = db
        self.bookingid = bid
        self.appstarttime = appstarttime
        self.recordIntoDB()

    def getDuration(self):
                
        sql = f"SELECT MAX(seconds) as lastrecordedsecond FROM telemetry WHERE bookingid=%(bookingid)s"
        sqldata = {"bookingid": self.bookingid}

        result = self.mysqlm.retrieve(MySQLManager.QUERYTYPE_RETRIEVE, sql, sqldata)

        if result == True:
            record = self.mysqlm.cursor.fetchone()
            duration = record[0]
            return True,duration

        else:
            print(f"Error retrieving the data of booking id {self.bookingid}")
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            return False,-1


    def recordIntoDB(self):

        getDuration_isSuccessful, duration = self.getDuration()

        self.startdatetime_value = datetime.now()
        self.enddatetime_value = self.startdatetime_value + timedelta(seconds = duration)
        self.bookingidwithtime = f"{self.bookingid}_{str(self.appstarttime)}"

        mdtu = MyDateTimeUtilities()        
        self.offsetseconds = mdtu.date_diff_in_seconds(self.startdatetime_value-self.appstarttime)

        sql = "INSERT INTO socketfeedv2 (bookingid,bookingidwithtime,offsetseconds,startdatetime_value,enddatetime_value) VALUES (%(bookingid)s,%(bookingidwithtime)s,%(offsetseconds)s,%(startdatetime_value)s,%(enddatetime_value)s)"
        sqldata = {'bookingid': self.bookingid, 'bookingidwithtime': self.bookingidwithtime, 'offsettime': self.offsetseconds,
                   'startdatetime_value': self.startdatetime_value, 'enddatetime_value':self.enddatetime_value}        
        insert_isSuccessful = self.mysqlm.insertupdatedelete(MySQLManager.QUERYTYPE_INSERT,sql,sqldata)
        if insert_isSuccessful:
            print(f"{sqldata} inserted")


    def getBookingID(self):
        return self.bookingid 

