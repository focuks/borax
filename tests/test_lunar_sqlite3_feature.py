# coding=utf8

import sqlite3
import unittest

from borax.calendars.lunardate import LunarDate


def adapt_lunardate(ld):
    return ld.encode()


sqlite3.register_adapter(LunarDate, adapt_lunardate)
sqlite3.register_converter("lunardate", LunarDate.decode)


class Sqlite3CustomFieldTestCase(unittest.TestCase):
    def test_custom_field(self):
        con = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
        cur = con.cursor()
        cur.execute('CREATE TABLE member (pid INT AUTO_INCREMENT PRIMARY KEY,birthday lunardate);')
        ld = LunarDate(2018, 5, 3)
        cur.execute("INSERT INTO member(birthday) VALUES (?)", (ld,))
        cur.execute("SELECT pid, birthday FROM member;")
        my_birthday = cur.fetchone()[1]
        cur.close()
        con.close()
        self.assertEqual(LunarDate, type(my_birthday))
        self.assertEqual(2018, my_birthday.year)
        self.assertEqual(5, my_birthday.month)
        self.assertEqual(3, my_birthday.day)
        self.assertEqual(0, my_birthday.leap)
