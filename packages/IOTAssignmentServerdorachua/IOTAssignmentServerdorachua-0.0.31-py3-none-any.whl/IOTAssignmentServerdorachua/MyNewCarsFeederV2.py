import sys

from datetime import datetime
 
from datetime import timedelta  
from time import sleep
from IOTAssignmentUtilitiesdorachua import MySQLManager
from IOTAssignmentServerdorachua.GrabCarV2 import GrabCarV2

class MyNewCarsFeederV2:

    def __init__(self,u,pw,h,db,min,max,pbid):
        self.user = u
        self.password = pw
        self.host = h
        self.database = db
        self.isconnected = False
        self.min = min
        self.max = max
        self.permanentbookingid = pbid
        self.truncateDB()

    def setPermanentBookingID(self,bid):
        self.permanentbookingid = bid

    def setMinMax(self,min,max):
        self.min = min
        self.max = max

    def getRandomBookingIDs(self,numbertoget):

        bids = []    

        result = self.mysqlm.retrieve(MySQLManager.QUERYTYPE_RETRIEVE, f"SELECT bookingid FROM telemetry ORDER BY RAND() LIMIT {numbertoget}",{})

        if result == True:
            results = self.mysqlm.cursor.fetchall()

            for r in results:
                bids.append(r[0])                

        else:
            print(f"Error retrieving {numbertoget} random booking ids")

        return bids

    def getDurationInSecondsOfBookingID(self,bid):
                
        sql = f"SELECT MAX(seconds) as lastrecordedsecond FROM telemetry WHERE bookingid=%(bookingid)s"
        sqldata = {"bookingid": bid}

        result = self.mysqlm.retrieve(MySQLManager.QUERYTYPE_RETRIEVE, sql, sqldata)

        if result == True:
            record = self.mysqlm.cursor.fetchone()
            duration = record[0]
            return True,duration

        else:
            print(f"Error retrieving the data of booking id {bid}")
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            return False,-1


    def createCars(self,bids):

        try:

            cars = []

            datetime_start = datetime.now()
            
            for bid in bids:

                car = GrabCarV2(bid,self.user, self.password,self.host,self.database)
                cars.append(car)

                sql = "INSERT INTO socketfeed (bookingid,startdatetime_value,enddatetime_value) VALUES (%(bookingid)s,%(startdatetime_value)s,%(enddatetime_value)s)"
                
                getDurationOfBookingID_isSuccessful,duration = self.getDurationOfBookingID(bid)

                if getDurationOfBookingID_isSuccessful:
                
                    startdatetime_value = datetime_start
                    enddatetime_value = datetime_start + timedelta(seconds=duration)
                    
                    sqldata = {'bookingid': bid , 'startdatetime_value': startdatetime_value,'enddatetime_value': enddatetime_value } 
                    insert_isSuccessful = self.mysqlm.insertupdatedelete(MySQLManager.QUERYTYPE_INSERT,sql,sqldata)
                    if insert_isSuccessful:
                        print(f"{sqldata} inserted")
        
            return insert_isSuccessful, cars

        except:
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            return False


    def truncateDB(self):

        try:                    
            
            self.mysqlm =  MySQLManager.MySQLManager(self.user, self.password,self.host,self.database)
            self.mysqlm.connect()

            print("Truncating records from database first...")
            self.mysqlm.insertupdatedelete( MySQLManager.QUERYTYPE_DELETE, "DELETE FROM socketfeed",{})

            self.mysqlm.disconnect()

        except KeyboardInterrupt:
            print('Interrupted')
            sys.exit()

        except:
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])       

    def getCars(self):
        import random
        if self.min == None:
            self.min = 1
        if self.max == None:
            self.max = 3
        numcars = random.randint(self.min, self.max)
        self.getCars(numcars)
    

    def getCars(self,numcars):
        
        cars = []

        try:        
                        
            self.mysqlm =  MySQLManager.MySQLManager(self.user, self.password,self.host,self.database)
            self.mysqlm.connect()

            print(f"Getting {numcars} random IDs from database...")
            bids = self.getRandomBookingIDs(numcars-1)
            bids.append(self.permanentbookingid)
            print(bids)
            
            print("Creating new cars")
            populateSocketFeedTable_isSuccessful,cars = self.createCars(bids)  
        
            
            self.mysqlm.disconnect()

            return cars

        except KeyboardInterrupt:
            print('Interrupted')
            sys.exit()

        except:
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])