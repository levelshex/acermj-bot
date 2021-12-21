import sqlite3
from datetime import datetime


class DBHelper:
    def __init__(self, dbname="testbot.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)
        self.cur = self.conn.cursor()

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS bookings (date TEXT NOT NULL, booker TEXT, time_start TEXT NOT NULL, time_end TEXT NOT NULL, table_type TEXT CHECK( table_type IN ('auto','normal','other')) NOT NULL DEFAULT 'auto')"
        self.cur.execute(stmt)
        self.conn.commit()

    def add_booking(self, date, booker, time_start, time_end, table_type):
        stmt = f"INSERT INTO bookings (date, booker, time_start, time_end, table_type) VALUES (\"{date}\", \"@{booker}\", \"{time_start}\", \"{time_end}\", \"{table_type}\")"
        self.cur.execute(stmt)
        self.conn.commit()

    def delete_booking(self, date, booker, time_start, table):
        stmt = f"DELETE FROM bookings WHERE (?)"
        args = (date, booker, time_start, table)
        self.cur.execute(stmt, args)
        self.conn.commit()

    def get_bookings(self):
        self.cur.execute("SELECT * FROM bookings WHERE table_type = \"auto\" ORDER BY date, time_start")
        auto = self.cur.fetchall()
        self.cur.execute("SELECT * FROM bookings WHERE table_type = \"normal\" ORDER BY date, time_start")
        normal = self.cur.fetchall()
        self.cur.execute("SELECT * FROM bookings WHERE table_type = \"other\" ORDER BY date, time_start")
        other = self.cur.fetchall()
        return {"auto": auto,
                "normal": normal,
                "other": other}


def is_valid_add(arr):
    if is_valid_date(arr[0]) and is_valid_time(arr[1]) and is_valid_time(arr[2]) and is_valid_table(arr[3]):
        dbhelper = DBHelper()
        return dbhelper.get_bookings()


def is_valid_date(date):
    if datetime.strptime(date, "%Y-%m-%d"):
        return True
    else:
        return False


def is_valid_time(time):
    return len(time) == 5 and int(time[:1]) in range(24) and int(time[3:]) in range(60)


def is_valid_table(table_type):
    return table_type in ["auto", "normal", "other"]
