import sys
import mysql.connector
from IOTAssignmentUtilitiesdorachua import MyJSONHelper

QUERYTYPE_RETRIEVE = "RETRIEVE"
QUERYTYPE_INSERT= "INSERT"
QUERYTYPE_UPDATE = "UPDATE"
QUERYTYPE_DELETE = "DELETE"

class MySQLManager:

    def __init__(self,u,pw,h,db):
        self.user = u
        self.password = pw
        self.host = h
        self.database = db
        self.isconnected = False

    def connect(self):
        try:
            self.cnx = mysql.connector.connect(user=self.user,password=self.password,host=self.host,database=self.database) 
            self.cursor = self.cnx.cursor()
            self.isconnected = True
            #print("Successfully connected to database!")
            return True
            
        except:
            print("Error connecting to database")
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            self.isconnected = False
            return False

    def disconnect(self):
        try:
            if self.cursor is not None:
                self.cursor.close()
            if self.cnx is not None:
                self.cnx.close()            
            #print("Successfully disconnected from database")
            self.isconnected = False            
            return True

        except:
            print("Error disconnecting from database")
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            return True

    def checkexists(self,sql,data):
        try:
            self.cursor.execute(sql,data)
            if len(self.cursor)>0:
                return True
            else:
                return False
        except:
            print(f"Error checking if record exists")
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            return False

    def retrieve(self,querytype,sql,data):
        try:
            self.cursor.execute(sql,data)
            return True
        except:
            print(f"Error performing operation {querytype}")
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            return False
    
    def insertupdatedelete(self,querytype,sql,data):
        try:
            self.cursor.execute(sql,data)
            self.cnx.commit()
            return True
        except:
            print(f"Error performing operation {querytype}")
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            return False

    def fetch_fromdb_as_list(self,sql,datasql):
    
        try:
            self.cursor.execute(sql,datasql)
            row_headers=[x[0] for x in self.cursor.description] 
            results = self.cursor.fetchall()
            data = []
            for result in results:
                data.append(dict(zip(row_headers,result)))            
            
            return data

        except:
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            return None
			
    def fetch_fromdb_as_json(self,sql,datasql):
    
        try:
            self.cursor.execute(sql,datasql)
            row_headers=[x[0] for x in self.cursor.description] 
            results = self.cursor.fetchall()
            data = []
            for result in results:
                data.append(dict(zip(row_headers,result)))
            
            data_reversed = data[::-1]

            data = {'data':data_reversed}
            
            return MyJSONHelper.data_to_json(data)

        except:
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            return None