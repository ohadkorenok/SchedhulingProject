import os
import sqlite3
from create_db import *

if os.path.isfile("classes.db"):
    conn = sqlite3.connect("classes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    for i in cursor.fetchall():

