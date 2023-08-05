import sys

from datetime import datetime
from datetime import datetime  
from datetime import timedelta  
from time import sleep
from IOTAssignmentUtilitiesdorachua import MySQLManager
from IOTAssignmentServerdorachua.GrabCar import GrabCar

class MyNewCarsFeeder:

    def __init__(self,u,pw,h,db,min,max,bid):
        self.user = u
        self.password = pw
        self.host = h
        self.database = db
        self.isconnected = False
        self.min = min
        self.max = max
        self.permanentbookingid = bid

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
            print(f"Error retrieving 5 random booking ids")

        return bids

    def getDurationOfBookingID(self,bid,prevmax, prevbid):

        currentmax = prevmax
        currentbid = prevbid

        sql = f"SELECT MAX(seconds) as lastrecordedsecond FROM telemetry WHERE bookingid=%(bookingid)s"
        sqldata = {"bookingid": bid}

        result = self.mysqlm.retrieve(MySQLManager.QUERYTYPE_RETRIEVE, sql, sqldata)

        if result == True:
            record = self.mysqlm.cursor.fetchone()
            thismax = record[0]
            if thismax > prevmax:
                currentmax = thismax
                currentbid = bid
            return True, thismax,currentmax, currentbid

        else:
            print(f"Error retrieving the data of booking id {bid}")
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            return False, 0, currentmax, currentbid

    

    def populateSocketFeedTable(self,bids,datetime_start,prevmax,prevbid):

        currentmax = prevmax
        currentbid = prevbid
        
        #id,bookingid,startdatetime_value,enddatetime_value,timestamp_value
        for bid in bids:

            sql = "INSERT INTO socketfeed (bookingid,startdatetime_value,enddatetime_value) VALUES (%(bookingid)s,%(startdatetime_value)s,%(enddatetime_value)s)"
            #def getDurationOfBookingID(mysqlm,bid,prevmax, prevbid):
            success,seconds,currentmax,currentbid = self.getDurationOfBookingID(bid,prevmax,prevbid)
            prevmax = currentmax; prevbid = currentbid
            
            startdatetime_value = datetime_start
            enddatetime_value = datetime_start + timedelta(seconds=seconds)
            
            sqldata = {'bookingid': bid , 'startdatetime_value': startdatetime_value,'enddatetime_value': enddatetime_value } 
            success = self.mysqlm.insertupdatedelete(MySQLManager.QUERYTYPE_INSERT,sql,sqldata)
            if success:
                print(f"{sqldata} inserted")

        return currentmax, datetime_start + timedelta(seconds=currentmax), currentbid


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

            self.truncateDB()
                        
            self.mysqlm =  MySQLManager.MySQLManager(self.user, self.password,self.host,self.database)
            self.mysqlm.connect()

            print(f"Getting {numcars} random IDs from database...")
            bids = self.getRandomBookingIDs(numcars-1)
            bids.append(self.permanentbookingid)
            print(bids)

            datetime_start = datetime.now()
            print("Inserting new data into socketfeed database")
            currentmax,next_feed_time,currentbid = self.populateSocketFeedTable(bids,datetime_start,0,0)  

            print(f"Waiting for {currentmax} seconds until next round of feeding at {next_feed_time} by {currentbid}")            

            for bid in bids:
                cars.append(GrabCar(bid,self.user, self.password,self.host,self.database))
            
            
            self.mysqlm.disconnect()

            return cars, currentmax,next_feed_time, currentbid

        except KeyboardInterrupt:
            print('Interrupted')
            sys.exit()

        except:
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])      
