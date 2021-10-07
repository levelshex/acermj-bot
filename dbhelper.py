import sqlite3

class DBHelper:
    def __init__(self, dbname="acermj.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)
    
    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS bookings 
        \(time datetime, booker varchar(50), timing string check(timing = 'morning' or timing='afternoon' or timing='night' or timing='midnight)"
    
    def add_booking(self, time, booker, timing):
        stmt = f"INSERT INTO bookings ({time}, {booker}, {timing})"
        self.conn.execute(stmt)
        self.conn.commit()
    
    def delete_booking(self, time, booker, timing):
        stmt = f"DELETE FROM bookings WHERE (?)"
        args = (time, booker, timing)
        self.conn.execute(stmt, args)
        self.conn.commit()
    
    def get_bookings(self):
        stmt = "SELECT * FROM bookings"
        return self.conn.execute(stmt)