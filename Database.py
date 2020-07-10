import sqlite3
import datetime
import sys

class Handler():    
    def __init__(self, database_path):
        self.databaseConn = sqlite3.connect(database_path)
        self.databaseCursor=self.databaseConn.cursor()

        self.databaseCursor.execute("""CREATE TABLE if not exists network (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                domain TEXT DEFAULT NULL,
                                ip_addr TEXT DEFAULT NULL,
                                first_seen timestamp DEFAULT NULL,
                                last_seen timestamp DEFAULT NULL,
                                traffic_from INTEGER DEFAULT 0,
                                traffic_to INTEGER DEFAULT 0,
                                req_count INTEGER DEFAULT 0
                            )""")


    def insertNew(self, domain):
        today = datetime.datetime.now()
        self.databaseCursor.execute("INSERT INTO network (domain, first_seen, last_seen, req_count) VALUES (?,?,?,1)", (domain, today, today,))
        self.databaseConn.commit()

    def checkDomain(self, domain):
        self.databaseCursor.execute("SELECT domain FROM network WHERE domain=?", (domain,))
        result = self.databaseCursor.fetchone()
        if result:
            return True
        else: return False

    def checkIP(self, ip):
        self.databaseCursor.execute("SELECT domain FROM network WHERE ip_addr=?", (ip,))
        result = self.databaseCursor.fetchone()
        return result

    def setIPAddress(self, ip, domain):
        self.databaseCursor.execute("UPDATE network SET ip_addr=? WHERE domain=?", (ip, domain,))
        self.databaseConn.commit()        

    def updateCount(self, domain):
        self.databaseCursor.execute("UPDATE network SET req_count = req_count+1,last_seen=? WHERE domain=?;", (datetime.datetime.now(), domain,))
        self.databaseConn.commit()

    def updateTraffic(self, domain, direction, nbytes):
        if(direction=="out"):
            self.databaseCursor.execute("UPDATE network SET traffic_to=traffic_to+? WHERE domain=?;", (nbytes, domain,))
        else:
             self.databaseCursor.execute("UPDATE network SET traffic_from=traffic_from+? WHERE domain=?;", (nbytes, domain,))
        
        self.databaseConn.commit()

    def printTable(self):
        self.databaseCursor.execute("SELECT * FROM network")
        for tup in self.databaseCursor.fetchall():
            count = 0
            ip = "unknown"
            if tup[7]!=None: count=tup[7]
            if tup[2]!=None: ip=tup[2]
            line = "{}\t{:50s}\t{:15s}\t{:15s}\t{}\t{}\t{}\t{}".format(tup[0],tup[1],ip,str(tup[3]),str(tup[4]),str(tup[5]),str(tup[6]),count)
            print(line)
        print("-"*50)
