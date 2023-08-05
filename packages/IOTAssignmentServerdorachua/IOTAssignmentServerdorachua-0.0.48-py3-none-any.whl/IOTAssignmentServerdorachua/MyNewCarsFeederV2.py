import sys

from datetime import datetime
 
from datetime import timedelta  
from time import sleep
from IOTAssignmentUtilitiesdorachua.MySQLManager import MySQLManager
from IOTAssignmentUtilitiesdorachua.MySQLManager import QUERYTYPE_DELETE,QUERYTYPE_RETRIEVE
from IOTAssignmentServerdorachua.GrabCarV2 import GrabCarV2
from IOTAssignmentServerdorachua.SocketFeedV2 import SocketFeedV2

class MyNewCarsFeederV2:

    def __init__(self,u,pw,h,db):
        self.user = u
        self.password = pw
        self.host = h
        self.database = db
    
    
    def getRandomBookingIDs(self,numbertoget):

        bids = []

        try:

            self.mysqlm =  MySQLManager(self.user, self.password,self.host,self.database)
            self.mysqlm.connect()

            result = self.mysqlm.retrieve(QUERYTYPE_RETRIEVE, f"SELECT bookingid FROM telemetry ORDER BY RAND() LIMIT {numbertoget}",{})

            if result == True:
                results = self.mysqlm.cursor.fetchall()

                for r in results:
                    bids.append(r[0])                
            else:
                print(f"Error retrieving {numbertoget} random booking ids")

        except:
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])

        finally:
            self.mysqlm.disconnect()

        return bids
    
    def createCars(self,numbertoget):

        try:
            cars = []

            datetime_start = datetime.now()

            bids = self.getRandomBookingIDs(numbertoget)
            
            for bid in bids:
                car = GrabCarV2(datetime.now(),bid,self.user, self.password,self.host,self.database)                
                car.recordIntoDB()
                cars.append(car)            
        
            return cars

        except:
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            return cars

    def getAllCars(self):

        try:
            socketfeedv2 = []

            self.mysqlm =  MySQLManager(self.user, self.password,self.host,self.database)
            self.mysqlm.connect()

            sql = f"SELECT * FROM socketfeedv2"
            sqldata = {}
            self.mysqlm.retrieve(QUERYTYPE_RETRIEVE,sql,sqldata)
            records = self.mysqlm.fetch_fromdb_as_list(sql,sqldata)

            for r in records:
                sfv2 = SocketFeedV2(r,self.user, self.password,self.host,self.database)
                socketfeedv2.append(sfv2)

            self.mysqlm.disconnect()

            return socketfeedv2

        except:
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            return cars


    def truncateDB(self):

        try:                    
            
            self.mysqlm =  MySQLManager(self.user, self.password,self.host,self.database)
            self.mysqlm.connect()

            print("Truncating records from database first...")
            self.mysqlm.insertupdatedelete(QUERYTYPE_DELETE, "DELETE FROM socketfeedv2",{})

            self.mysqlm.disconnect()

        except KeyboardInterrupt:
            print('Interrupted')
            sys.exit()

        except:
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])